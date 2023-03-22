from dataclasses import dataclass, field


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        # Оставил метод для тестов.
        return self.__repr__()

    def __repr__(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int  # count
    duration: float  # hours
    weight: float  # kg
    M_IN_KM: int = field(init=False, default=1000)
    MIN_IN_H: int = field(init=False, default=60)
    LEN_STEP: int = field(init=False, default=.65)  # m

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/час."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # Abstract
        # Метод имплементируется в дочерних классах.
        raise NotImplementedError('Method not implemented.')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = field(init=False, default=18)
    CALORIES_MEAN_SPEED_SHIFT: float = field(init=False, default=1.79)

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * (self.duration * self.MIN_IN_H))


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float  # cm
    CALORIES_SPEND_WEIGHT_MULTIPLIER: float = field(init=False, default=.035)
    CALORIES_SPEND_UNKNOWN_MULTIPLIER: float = field(init=False, default=.029)
    KM_H_TO_M_SEC: float = field(init=False, default=.278)
    CM_IN_M: float = field(init=False, default=100)

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_SPEND_WEIGHT_MULTIPLIER * self.weight
                 + ((self.get_mean_speed() * self.KM_H_TO_M_SEC) ** 2
                    / (self.height / self.CM_IN_M))
                 * self.CALORIES_SPEND_UNKNOWN_MULTIPLIER * self.weight)
                * (self.duration * self.MIN_IN_H))


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    count_pool: int  # count
    length_pool: float  # m
    LEN_STEP: float = field(init=False, default=1.38)
    CALORIES_MEAN_SPEED_MULTIPLIER: float = field(init=False, default=1.1)
    CALORIES_SPEND_UNKNOWN_MULTIPLIER: float = field(init=False, default=2)

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_MULTIPLIER)
                * self.CALORIES_SPEND_UNKNOWN_MULTIPLIER
                * self.weight
                * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    available_trainings = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }

    if workout_type not in available_trainings.keys():
        raise ValueError(f'Unknown training type: "{workout_type}"')

    return available_trainings[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
