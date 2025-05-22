from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from database.models import Exercise
from schemas import (
    CreateExerciseRequest,
    CreateExerciseResponse,
    DeleteExerciseResponse,
    DetailExerciseResponse,
    ExerciseResponse,
    UpdateExerciseRequest,
    UpdateExerciseResponse,
)
from service_logging import logger

from .utils.pagination import PaginatedResponse, Pagination

router = APIRouter()


@router.get("/", summary="Получить список всех упражнений")
async def get_exercises(
    pg: Annotated[Pagination, Depends()],
    db: AsyncSession = Depends(get_db),
) -> PaginatedResponse[ExerciseResponse]:
    """Постранично возвращает список всех обучающих упражнений."""
    logger.info("Getting the exercise list...")
    stmt = select(Exercise).offset(pg.skip).limit(pg.size)
    result = await db.execute(stmt)
    exercises = result.scalars().all()

    stmt = select(func.count()).select_from(Exercise)
    result = await db.execute(stmt)
    total = result.scalar_one()

    items = [ExerciseResponse.model_validate(exercise) for exercise in exercises]
    logger.success(f"Received {len(items)} exercises.")

    return PaginatedResponse[ExerciseResponse](
        items=items,
        page=pg.page,
        size=pg.size,
        total=total,
    )


@router.get("/{uuid}", summary="Получить детальную информацию об упражнении")
async def get_exercise(
    uuid: Annotated[UUID, Path(...)],
    db: AsyncSession = Depends(get_db),
) -> DetailExerciseResponse:
    """Возвращает полную информацию о конкретном упражнении по его UUID."""
    logger.info("Getting information about an exercise...")
    stmt = select(Exercise).where(Exercise.id == uuid)
    result = await db.execute(stmt)
    exercise = result.scalar_one_or_none()

    if exercise is None:
        detail = "Exercise not found."
        logger.error(detail)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )

    item = DetailExerciseResponse.model_validate(exercise)
    logger.success(f"Exercise received: ({item.seq_number}){item.id}")

    return item


@router.post("/", summary="Добавить упражнение в систему")
async def create_text(
    data: Annotated[CreateExerciseRequest, Body(...)],
    db: AsyncSession = Depends(get_db),
) -> CreateExerciseResponse:
    """Добавляет новое упражнение в систему."""

    logger.info("Creating an exercise...")
    try:
        exercise = Exercise(
            title=data.title,
            difficulty=data.difficulty,
            tags=data.tags,
            text_id=data.text_id,
        )
        db.add(exercise)
        await db.commit()
        await db.refresh(exercise)

    except IntegrityError:
        await db.rollback()
        detail = "Exercise with this data already exists."
        logger.error(detail)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )

    except Exception as error:
        await db.rollback()
        detail = f"An error ocured while creating exercise: {error}"
        logger.error(detail)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )

    item = CreateExerciseResponse.model_validate(exercise)
    logger.success(f"Exercise has been created: ({item.seq_number}){item.id}")

    return item


@router.delete("/{uuid}", summary="Удалить упражнение из системы")
async def delete_text(
    uuid: Annotated[UUID, Path(...)],
    db: AsyncSession = Depends(get_db),
) -> DeleteExerciseResponse:
    """Удаляет упражнение из системы по его UUID."""
    logger.info("Deleting an exercise...")
    stmt = select(Exercise).where(Exercise.id == uuid)
    result = await db.execute(stmt)
    exercise = result.scalar_one_or_none()

    if exercise is None:
        detail = "Exercise not found."
        logger.error(detail)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )

    await db.delete(exercise)
    await db.commit()

    item = DeleteExerciseResponse.model_validate(exercise)
    logger.success(f"Exercise has been deleted: ({item.seq_number}){item.id}")

    return item


@router.patch("/{uuid}", summary="Обновить данные об упражнении")
async def update_text(
    uuid: Annotated[UUID, Path(...)],
    data: Annotated[UpdateExerciseRequest, Body(...)],
    db: AsyncSession = Depends(get_db),
) -> UpdateExerciseResponse:
    """Обновляет данные упражнения по его UUID."""
    logger.info("Updating an exercise...")
    stmt = select(Exercise).where(Exercise.id == uuid)
    result = await db.execute(stmt)
    exercise = result.scalar_one_or_none()

    if exercise is None:
        detail = "Exercise not found."
        logger.error(detail)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found.",
        )

    try:
        data = data.model_dump(exclude_none=True)
        for field in data:
            setattr(exercise, field, data[field])

        db.add(exercise)
        await db.commit()
        await db.refresh(exercise)

    except IntegrityError:
        await db.rollback()
        detail = "Exercise with this data already exists."
        logger.error(detail)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )

    except Exception as error:
        await db.rollback()
        detail = f"An error ocured while updating exercise: {error}"
        logger.error(detail)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )
    item = UpdateExerciseResponse.model_validate(exercise)
    logger.success(f"Exercise has been updated: ({item.seq_number}){item.id}")

    return item
