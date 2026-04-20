
import random
import math

# настройки
T_MODEL_HOURS = 24 * 30      # Время моделирования: 30 суток (720 часов)
LAMBDA = 1 / 8               # Интенсивность прихода составов: 1/8 состава в час
ALPHA = 0.95                 # Доверительная вероятность
EPS = 0.2                    # Требуемая точность 20%
TA = 1.96                    # Квантиль нормального распределения для ALPHA=0.95


# генераторы случ чисел
def exp_random(mean: float) -> float:
    """Экспоненциальное распределение с заданным средним"""
    return -mean * math.log(1 - random.random())


def uniform_int_random(a: int, b: int) -> int:
    """Равномерное распределение целых чисел на [a, b] (включительно)"""
    return random.randint(a, b)


def normal_random(mean: float, std: float) -> float:
    """Нормальное распределение (метод Бокса-Мюллера)"""
    u1 = random.random()
    u2 = random.random()
    z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
    return mean + std * z


def poisson_random(lam: float) -> int:
    """Распределение Пуассона (метод Кнута)"""
    L = math.exp(-lam)
    k = 0
    p = 1.0
    while p > L:
        k += 1
        p *= random.random()
    return k - 1


# имитационная модель
class SortingStation:
    """Модель сортировочной станции"""

    def __init__(self, num_tracks: int):
        self.num_tracks = num_tracks
        self.tracks_free_time = [0.0] * num_tracks
        self.section_queue = []
        self.accumulation = [0] * 8
        self.total_wagons = 0
        self.total_residence_time = 0.0
        self.composition_count = 0

    def _get_free_track(self) -> int:
        """Найти первую свободную ветку. Возвращает -1, если все заняты"""
        current_time = self.current_time
        for i, free_time in enumerate(self.tracks_free_time):
            if free_time <= current_time:
                return i
        return -1

    def _get_earliest_track(self):
        """Найти ветку, которая освободится раньше всех"""
        earliest_time = float('inf')
        earliest_idx = -1
        for i, free_time in enumerate(self.tracks_free_time):
            if free_time < earliest_time:
                earliest_time = free_time
                earliest_idx = i
        return earliest_idx, earliest_time

    def _process_section(self, wagon_count: int, direction: int, processing_time: float, arrival_time: float):
        """Обработать одну секцию"""
        current_time = self.current_time

        track_idx = self._get_free_track()

        if track_idx >= 0:
            start_time = current_time
            self.tracks_free_time[track_idx] = start_time + processing_time
        else:
            track_idx, free_time = self._get_earliest_track()
            start_time = free_time
            self.tracks_free_time[track_idx] = start_time + processing_time

        self.accumulation[direction] += wagon_count
        residence_time = (start_time + processing_time) - arrival_time
        self.total_residence_time += wagon_count * residence_time
        self.total_wagons += wagon_count

    def _try_form_composition(self):
        """Проверить и сформировать состав при накоплении >= 50"""
        for direction in range(1, 8):
            if self.accumulation[direction] >= 50:
                self.composition_count += 1
                self.accumulation[direction] = 0
                return True
        return False

    def run(self, simulation_time: float, train_arrival_times: list) -> dict:
        """Запуск моделирования"""
        self.current_time = 0.0
        self.total_wagons = 0
        self.total_residence_time = 0.0
        self.composition_count = 0
        self.tracks_free_time = [0.0] * self.num_tracks
        self.section_queue = []
        self.accumulation = [0] * 8

        for arrival_time in sorted(train_arrival_times):
            if arrival_time > simulation_time:
                break

            self.current_time = arrival_time

            # Генерация состава
            num_sections = uniform_int_random(2, 7)

            sections_data = []
            for _ in range(num_sections):
                wagon_count = poisson_random(3)
                if wagon_count == 0:
                    wagon_count = 1

                direction = random.randint(1, 7)

                # Время расцепки
                if random.random() < 0.1:
                    uncoupling_min = 30.0
                else:
                    uncoupling_min = normal_random(5.0, 2.0)
                    uncoupling_min = max(1.0, uncoupling_min)

                uncoupling_hours = uncoupling_min / 60.0
                moving_hours = 0.5  # 2 км / 4 км/ч
                processing_time = uncoupling_hours + moving_hours

                sections_data.append((wagon_count, direction, processing_time))

            # Обработка секций
            for wc, direc, proc_time in sections_data:
                self._process_section(wc, direc, proc_time, arrival_time)
                self._try_form_composition()

            while self._try_form_composition():
                pass

        if self.total_wagons == 0:
            avg_residence_time = 0
        else:
            avg_residence_time = self.total_residence_time / self.total_wagons

        return {
            'avg_residence_time': avg_residence_time,
            'total_wagons': self.total_wagons,
            'compositions': self.composition_count,
            'tracks': self.num_tracks
        }


# расчёт N*
def calculate_required_runs(num_tracks: int, initial_runs: int, epsilon: float, ta: float):
    """Алгоритм подбора числа реализаций N*"""
    N = initial_runs
    iteration = 0
    max_iterations = 10

    while iteration < max_iterations:
        iteration += 1

        results = []
        for _ in range(N):
            train_times = []
            current_time = 0
            while current_time < T_MODEL_HOURS:
                current_time += exp_random(1 / LAMBDA)
                if current_time < T_MODEL_HOURS:
                    train_times.append(current_time)

            station = SortingStation(num_tracks=num_tracks)
            res = station.run(T_MODEL_HOURS, train_times)
            results.append(res['avg_residence_time'])

        mean_res = sum(results) / N
        variance = sum((x - mean_res) ** 2 for x in results) / N
        sigma = math.sqrt(variance)

        N_star = int(math.ceil((sigma ** 2 * ta ** 2) / (epsilon ** 2)))

        print(f"  Итерация {iteration}: N={N}, sigma={sigma:.4f} ч, N*={N_star}")

        if N_star <= N:
            print(f"  Точность достигнута!")
            return N_star, mean_res, sigma
        else:
            print(f"  Точность не достигнута. Увеличиваем N до {N_star}")
            N = N_star

    return N, 0, 0


# основная программа
def main():
    print(f"Время моделирования: {T_MODEL_HOURS} ч ({T_MODEL_HOURS/24:.0f} сут)")
    print(f"Точность: {EPS*100}%, довер.вероятность: {ALPHA}, tα={TA}")

    print("эксперимент 1: 4 ветки")

    N_opt_4, mean_4, sigma_4 = calculate_required_runs(4, 50, EPS, TA)

    # прогон для 4 веток
    all_results_4 = []
    for _ in range(N_opt_4):
        train_times = []
        current_time = 0
        while current_time < T_MODEL_HOURS:
            current_time += exp_random(1 / LAMBDA)
            if current_time < T_MODEL_HOURS:
                train_times.append(current_time)
        station = SortingStation(4)
        res = station.run(T_MODEL_HOURS, train_times)
        all_results_4.append(res['avg_residence_time'])

    final_mean_4 = sum(all_results_4) / N_opt_4
    final_std_4 = math.sqrt(sum((x - final_mean_4) ** 2 for x in all_results_4) / N_opt_4)

    print(f"\nРезультаты для 4 веток:")
    print(f"  Число реализаций: {N_opt_4}")
    print(f"  Среднее время пребывания вагона: {final_mean_4:.2f} ч ({final_mean_4*60:.1f} мин)")
    print(f"  СКО: {final_std_4:.4f} ч")
    print(f"  Относительная погрешность: {final_std_4/final_mean_4*100:.2f}%")

    print("эксперимент 2: 5 веток")

    N_opt_5, mean_5, sigma_5 = calculate_required_runs(5, 50, EPS, TA)

    all_results_5 = []
    for _ in range(N_opt_5):
        train_times = []
        current_time = 0
        while current_time < T_MODEL_HOURS:
            current_time += exp_random(1 / LAMBDA)
            if current_time < T_MODEL_HOURS:
                train_times.append(current_time)
        station = SortingStation(5)
        res = station.run(T_MODEL_HOURS, train_times)
        all_results_5.append(res['avg_residence_time'])

    final_mean_5 = sum(all_results_5) / N_opt_5
    final_std_5 = math.sqrt(sum((x - final_mean_5) ** 2 for x in all_results_5) / N_opt_5)

    print(f"\nРезультаты для 5 веток:")
    print(f"  Число реализаций: {N_opt_5}")
    print(f"  Среднее время пребывания вагона: {final_mean_5:.2f} ч ({final_mean_5*60:.1f} мин)")
    print(f"  СКО: {final_std_5:.4f} ч")
    print(f"  Относительная погрешность: {final_std_5/final_mean_5*100:.2f}%")

    print("Анализ результатов")

    improvement = (final_mean_4 - final_mean_5) / final_mean_4 * 100
    print(f"Добавление 5-й ветки снизило время пребывания вагона на {improvement:.1f}%")
    print(f"  Было (4 ветки): {final_mean_4:.2f} ч ({final_mean_4*60:.1f} мин)")
    print(f"  Стало (5 веток): {final_mean_5:.2f} ч ({final_mean_5*60:.1f} мин)")


if __name__ == "__main__":
    main()