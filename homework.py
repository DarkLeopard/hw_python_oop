class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.calories: float = calories
        self.speed: float = speed
        self.distance: float = distance
        self.training_type: str = training_type
        self.duration: float = duration

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60
    LEN_STEP: int = .65  # m
    TRAINING_TYPE: str = None  # abstract

    def __init__(self,
                 action: int,  # count
                 duration: float,  # hours
                 weight: float,  # kg
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в км/час."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # abstract method
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.TRAINING_TYPE,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79
    TRAINING_TYPE: str = 'Running'

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * (self.duration * self.MIN_IN_H))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    TRAINING_TYPE: str = 'SportsWalking'
    CALORIES_SPEND_WEIGHT_MULTIPLIER: float = .035
    CALORIES_SPEND_UNKNOWN_MULTIPLIER: float = .029
    KM_H_TO_M_SEC = .278
    CM_IN_M = 100

    def __init__(self,
                 action: int,  # see parent
                 duration: float,  # see parent
                 weight: float,  # see parent
                 height: float) -> None:  # cm
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_SPEND_WEIGHT_MULTIPLIER * self.weight
                 + ((self.get_mean_speed() * self.KM_H_TO_M_SEC) ** 2
                    / (self.height / self.CM_IN_M))
                 * self.CALORIES_SPEND_UNKNOWN_MULTIPLIER * self.weight)
                * (self.duration * self.MIN_IN_H))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    TRAINING_TYPE: str = 'Swimming'
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 1.1
    CALORIES_SPEND_UNKNOWN_MULTIPLIER: float = 2

    def __init__(self,
                 action: int,  # see parent
                 duration: float,  # see parent
                 weight: float,  # see parent
                 length_pool: float,  # m
                 count_pool: int) -> None:  # count
        super().__init__(action, duration, weight)
        self.count_pool: int = count_pool
        self.length_pool: float = length_pool

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

    if workout_type in available_trainings.keys():
        return available_trainings[workout_type](*data)
    else:
        raise ValueError(f'Unknown training type: "{workout_type}"')


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
