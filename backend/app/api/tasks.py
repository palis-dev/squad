from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.orchestrator import SquadOrchestrator
from app.models.artifact import Artifact
from app.models.database import get_db
from app.models.message import Message
from app.models.task import Task, TaskStatus
from app.schemas.artifact import ArtifactResponse
from app.schemas.message import MessageResponse
from app.schemas.task import TaskCreate, TaskListResponse, TaskResponse, TaskUpdate

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

orchestrator = SquadOrchestrator()


@router.post("", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
):
    task = Task(
        title=task_data.title,
        description=task_data.description,
        acceptance_criteria=task_data.acceptance_criteria,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    status: Optional[TaskStatus] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    query = select(Task)
    if status:
        query = query.where(Task.status == status)
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    tasks = result.scalars().all()
    
    count_query = select(Task)
    if status:
        count_query = count_query.where(Task.status == status)
    count_result = await db.execute(count_query)
    total = len(count_result.scalars().all())
    
    return TaskListResponse(tasks=tasks, total=total)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    await db.commit()
    await db.refresh(task)
    return task


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    await db.delete(task)
    await db.commit()
    return {"message": "Task deleted successfully"}


@router.post("/{task_id}/run")
async def run_task(
    task_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.status == TaskStatus.IN_PROGRESS:
        raise HTTPException(status_code=400, detail="Task is already running")
    
    task.status = TaskStatus.IN_PROGRESS
    await db.commit()
    
    background_tasks.add_task(
        execute_task_workflow,
        task_id,
        task.description or task.title,
    )
    
    return {"message": "Task execution started", "task_id": task_id}


async def execute_task_workflow(task_id: int, task_description: str):
    try:
        await orchestrator.run(task_id, task_description)
    except Exception as e:
        print(f"Error executing task {task_id}: {e}")


@router.get("/{task_id}/messages", response_model=List[MessageResponse])
async def get_task_messages(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    result = await db.execute(
        select(Message)
        .where(Message.task_id == task_id)
        .order_by(Message.created_at)
    )
    messages = result.scalars().all()
    return messages


@router.get("/{task_id}/artifacts", response_model=List[ArtifactResponse])
async def get_task_artifacts(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    result = await db.execute(
        select(Artifact)
        .where(Artifact.task_id == task_id)
        .order_by(Artifact.created_at)
    )
    artifacts = result.scalars().all()
    return artifacts
