from dataclasses import asdict, dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """
    Класс для создания объектов сообщений.
    Информационное сообщение о тренировке.
    """

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    # числовые значения округляются при выводе до тысячных долей с помощью
    # format specifier (.3f)
    def get_message(self) -> str:
        """Метод возвращает строку сообщения"""
        return self.message.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float

    LEN_STEP = 0.65
    M_IN_KM = 1000

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    action: int
    duration: float
    weight: float
    height: float

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * (self.duration / 60))


@dataclass
class SportsWalking(Training):

    action: int
    duration: float
    weight: float
    height: float

    CALORIES_M = 0.035
    CALORIES_H = 0.029
    SECONDS = 60

    def get_spent_calories(self) -> float:
        return (self.CALORIES_M * self.weight + (self.get_mean_speed() ** 2
                // self.height)
                * self.CALORIES_H * self.weight
                * (self.duration / self.SECONDS))
    """Тренировка: спортивная ходьба."""
    pass


@dataclass
class Swimming(Training):
    LEN_STEP = 1.38

    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: float
    """Тренировка: плавание."""


def get_mean_speed(self) -> float:
    return (self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration)


def get_spent_calories(self) -> float:
    return ((self.get_mean_speed() + 1.1) * 2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type not in workout:
        raise ValueError('Ошибка.')
    return workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
