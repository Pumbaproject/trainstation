
import random
import math

T_MODEL_HOURS = 24 * 30      # Время моделирования: 30 суток (720 часов)
LAMBDA = 1 / 8               # Интенсивность прихода составов: 1/8 состава в час
ALPHA = 0.95                 # Доверительная вероятность
EPS = 0.2                    # Требуемая точность 20%
TA = 1.96                    # Квантиль для ALPHA=0.95


# генератор случ чисел
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


def get_uncoupling_time() -> float:
    """Генерация времени расцепки одной секции (часы)"""
    if random.random() < 0.1:
        uncoupling_min = 30.0
    else:
        uncoupling_min = normal_random(5.0, 2.0)
        uncoupling_min = max(1.0, uncoupling_min)
    return uncoupling_min / 60.0


# структура секции
class Section:
    """Секция вагонов"""
    def __init__(self, wagon_count: int, direction: int, is_urgent: bool, arrival_time: float):
        self.wagon_count = wagon_count      # количество вагонов
        self.direction = direction          # направление 1..7
        self.is_urgent = is_urgent          # срочность
        self.arrival_time = arrival_time    # время прибытия состава
        self.uncoupling_time = get_uncoupling_time()  # время расцепки
        self.moving_time = 2.0 / 4.0        # 2 км / 4 км/ч = 0.5 часа
        self.total_time = self.uncoupling_time + self.moving_time  # общее время обработки


# имитационная модель
class SortingStation:
    """Модель сортировочной станции"""

    def __init__(self, num_tracks: int):
        self.num_tracks = num_tracks

        self.tracks_free_time = [0.0] * num_tracks

        self.accumulation = [0] * 8

        self.urgent_direction = None

        self.direction_queue = list(range(1, 8))
        self.direction_queue_index = 0

        self.total_wagons = 0
        self.total_residence_time = 0.0
        self.composition_count = 0
        self.current_time = 0.0

        self.total_busy_time = 0.0

    def _get_free_track(self):
        """Найти первую свободную ветку. Возвращает индекс или -1"""
        for i, free_time in enumerate(self.tracks_free_time):
            if free_time <= self.current_time:
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

    def _get_next_direction(self):
        """Получить следующее направление из очереди (циклическая)"""
        direction = self.direction_queue[self.direction_queue_index]
        self.direction_queue_index = (self.direction_queue_index + 1) % len(self.direction_queue)
        return direction

    def _process_section(self, section: Section):
        """Обработать одну секцию: занять ветку, обновить накопление"""

        track_idx = self._get_free_track()

        if track_idx >= 0:
            start_time = self.current_time
            self.tracks_free_time[track_idx] = start_time + section.total_time
        else:
            track_idx, free_time = self._get_earliest_track()
            start_time = free_time
            self.tracks_free_time[track_idx] = start_time + section.total_time

        self.total_busy_time += section.total_time

        self.accumulation[section.direction] += section.wagon_count

        if section.is_urgent:
            self.urgent_direction = section.direction

        # Время пребывания вагонов
        finish_time = start_time + section.total_time
        residence_time = finish_time - section.arrival_time
        self.total_residence_time += section.wagon_count * residence_time
        self.total_wagons += section.wagon_count

    def _try_form_composition(self):
        """Проверить и сформировать состав при накоплении >= 50"""
        formed = False

        if self.urgent_direction is not None:
            if self.accumulation[self.urgent_direction] >= 50:
                self.composition_count += 1
                self.accumulation[self.urgent_direction] = 0
                self.urgent_direction = None
                formed = True
                return True

        for direction in range(1, 8):
            if self.accumulation[direction] >= 50:
                self.composition_count += 1
                self.accumulation[direction] = 0
                formed = True

        return formed

    def _generate_train_sections(self, arrival_time: float) -> list:
        """Генерация всех секций одного состава"""
        num_sections = uniform_int_random(2, 7)
        sections = []

        for _ in range(num_sections):
            wagon_count = poisson_random(3)
            if wagon_count == 0:
                wagon_count = 1

            direction = random.randint(1, 7)
            is_urgent = random.random() < 0.05

            sections.append(Section(wagon_count, direction, is_urgent, arrival_time))

        return sections

    def _generate_train_arrival_times(self) -> list:
        """Генерация всех времён прихода составов"""
        times = []
        current_time = 0
        while current_time < T_MODEL_HOURS:
            current_time += exp_random(1 / LAMBDA)
            if current_time < T_MODEL_HOURS:
                times.append(current_time)
        return times

    def run(self) -> dict:
        """Запуск моделирования"""
        # Сброс состояния
        self.current_time = 0.0
        self.total_wagons = 0
        self.total_residence_time = 0.0
        self.composition_count = 0
        self.total_busy_time = 0.0
        self.tracks_free_time = [0.0] * self.num_tracks
        self.accumulation = [0] * 8
        self.urgent_direction = None
        self.direction_queue = list(range(1, 8))
        self.direction_queue_index = 0

        # Генерация всех приходов составов
        arrival_times = self._generate_train_arrival_times()

        # Обработка каждого состава
        for arrival_time in arrival_times:
            self.current_time = arrival_time

            # Генерация секций состава
            sections = self._generate_train_sections(arrival_time)

            # Обработка секций
            for section in sections:
                self._process_section(section)
                self._try_form_composition()

            self._try_form_composition()

        # Расчёт итоговых показателей
        if self.total_wagons == 0:
            avg_residence_time = 0
            avg_track_load = 0
        else:
            avg_residence_time = self.total_residence_time / self.total_wagons
            avg_track_load = self.total_busy_time / (self.num_tracks * T_MODEL_HOURS) * 100

        return {
            'avg_residence_time': avg_residence_time,
            'total_wagons': self.total_wagons,
            'compositions': self.composition_count,
            'avg_track_load': avg_track_load,
            'tracks': self.num_tracks
        }


# расчёт N*
def calculate_required_runs(num_tracks: int, initial_runs: int, epsilon: float, ta: float):
    """Алгоритм подбора числа реализаций N*"""
    N = initial_runs
    iteration = 0
    max_iterations = 5

    while iteration < max_iterations:
        iteration += 1

        results = []
        for _ in range(N):
            station = SortingStation(num_tracks=num_tracks)
            res = station.run()
            results.append(res['avg_residence_time'])

        # Расчёт среднего и СКО
        mean_res = sum(results) / N
        variance = sum((x - mean_res) ** 2 for x in results) / N
        sigma = math.sqrt(variance)

        # Расчёт необходимого числа реализаций
        if sigma == 0:
            N_star = 1
        else:
            N_star = int(math.ceil((sigma ** 2 * ta ** 2) / (epsilon ** 2)))

        print(f"  Итерация {iteration}: N={N}, время={mean_res:.2f} ч, sigma={sigma:.4f} ч, N*={N_star}")

        if N_star <= N:
            print(f"  Точность достигнута!")
            return N_star, mean_res, sigma
        else:
            print(f"  Точность не достигнута. Увеличиваем N до {N_star}")
            N = N_star

    return N, 0, 0


# программа
def main():
    print(f"Время моделирования: {T_MODEL_HOURS} ч ({T_MODEL_HOURS/24:.0f} сут)")
    print(f"Интенсивность прихода составов: 1/{1/LAMBDA:.0f} час = {LAMBDA:.3f} состав/ч")
    print(f"Точность: {EPS*100}%, довер.вероятность: {ALPHA}, tα={TA}")

    print("Эксперимент 1: 4 ветки")

    N_opt_4, mean_4, sigma_4 = calculate_required_runs(4, 50, EPS, TA)

    # Финальный прогон для 4 веток
    all_results_4 = []
    all_compositions_4 = []
    all_load_4 = []
    for _ in range(max(N_opt_4, 10)):  # 10 прогонов для статистики
        station = SortingStation(4)
        res = station.run()
        all_results_4.append(res['avg_residence_time'])
        all_compositions_4.append(res['compositions'])
        all_load_4.append(res['avg_track_load'])

    final_mean_4 = sum(all_results_4) / len(all_results_4)
    final_compositions_4 = sum(all_compositions_4) / len(all_compositions_4)
    final_load_4 = sum(all_load_4) / len(all_load_4)
    final_std_4 = math.sqrt(sum((x - final_mean_4) ** 2 for x in all_results_4) / len(all_results_4))
    rel_error_4 = final_std_4 / final_mean_4 * 100

    print(f"\nРезультаты для 4 веток:")
    print(f"  Число реализаций: {len(all_results_4)}")
    print(f"  Среднее время пребывания вагона: {final_mean_4:.2f} ч ({final_mean_4*60:.1f} мин)")
    print(f"  Всего обработано вагонов (ср.): {final_mean_4 * T_MODEL_HOURS / final_mean_4:.0f}")
    print(f"  Сформировано составов (ср.): {final_compositions_4:.0f}")
    print(f"  Загрузка веток: {final_load_4:.1f}%")
    print(f"  СКО: {final_std_4:.4f} ч")
    print(f"  Относительная погрешность: {rel_error_4:.2f}%")

    print("Эксперимент 2: 5 веток")

    N_opt_5, mean_5, sigma_5 = calculate_required_runs(5, 50, EPS, TA)

    all_results_5 = []
    all_compositions_5 = []
    all_load_5 = []
    for _ in range(max(N_opt_5, 10)):
        station = SortingStation(5)
        res = station.run()
        all_results_5.append(res['avg_residence_time'])
        all_compositions_5.append(res['compositions'])
        all_load_5.append(res['avg_track_load'])

    final_mean_5 = sum(all_results_5) / len(all_results_5)
    final_compositions_5 = sum(all_compositions_5) / len(all_compositions_5)
    final_load_5 = sum(all_load_5) / len(all_load_5)
    final_std_5 = math.sqrt(sum((x - final_mean_5) ** 2 for x in all_results_5) / len(all_results_5))
    rel_error_5 = final_std_5 / final_mean_5 * 100

    print(f"\nРезультаты для 5 веток:")
    print(f"  Число реализаций: {len(all_results_5)}")
    print(f"  Среднее время пребывания вагона: {final_mean_5:.2f} ч ({final_mean_5*60:.1f} мин)")
    print(f"  Сформировано составов (ср.): {final_compositions_5:.0f}")
    print(f"  Загрузка веток: {final_load_5:.1f}%")
    print(f"  СКО: {final_std_5:.4f} ч")
    print(f"  Относительная погрешность: {rel_error_5:.2f}%")

    print("Анализ результатов")

    improvement = (final_mean_4 - final_mean_5) / final_mean_4 * 100
    print(f"Добавление 5-й ветки снизило время пребывания вагона на {improvement:.1f}%")
    print(f"  Было (4 ветки): {final_mean_4:.2f} ч ({final_mean_4*60:.1f} мин)")
    print(f"  Стало (5 веток): {final_mean_5:.2f} ч ({final_mean_5*60:.1f} мин)")

    print(f"\nЗагрузка веток:")
    print(f"  4 ветки: {final_load_4:.1f}%")
    print(f"  5 веток: {final_load_5:.1f}%")


if __name__ == "__main__":
    random.seed(42)
    main()