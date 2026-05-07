import station_simulation
import matplotlib.pyplot as plt
import math

# программа
def TestForks(T_MODEL_HOURS, LAMBDA, ALPHA, TA, EPS):
    print(f"Время моделирования: {T_MODEL_HOURS} ч ({T_MODEL_HOURS/24:.0f} сут)")
    print(f"Интенсивность прихода составов: 1/{1/LAMBDA:.0f} час = {LAMBDA:.3f} состав/ч")
    print(f"Точность: {EPS*100}%, довер.вероятность: {ALPHA}, tα={TA}")

    print("\nЭксперимент 1: 1 ветка")

    N_opt_1, mean_1, sigma_1 = station_simulation.calculate_required_runs(1, 50, EPS, TA)

    all_results_1 = []
    all_compositions_1 = []
    all_load_1 = []

    for _ in range(max(N_opt_1, 10)):
        station = station_simulation.SortingStation(1)

        res = station.run()

        all_results_1.append(res['avg_residence_time'])
        all_compositions_1.append(res['compositions'])
        all_load_1.append(res['avg_track_load'])

    final_mean_1 = sum(all_results_1) / len(all_results_1)
    final_compositions_1 = sum(all_compositions_1) / len(all_results_1)
    final_load_1 = sum(all_load_1) / len(all_results_1)

    print(f"\nРезультаты для 1 ветки:")
    print(f"  Среднее время пребывания вагона: {final_mean_1:.2f} ч")
    print(f"  Сформировано составов (ср.): {final_compositions_1:.0f}")
    print(f"  Загрузка веток: {final_load_1:.1f}%")


    print("\nЭксперимент 2: 2 ветки")

    N_opt_2, mean_2, sigma_2 = station_simulation.calculate_required_runs(2, 50, EPS, TA)

    all_results_2 = []
    all_compositions_2 = []
    all_load_2 = []

    for _ in range(max(N_opt_2, 10)):
        station = station_simulation.SortingStation(2)

        res = station.run()

        all_results_2.append(res['avg_residence_time'])
        all_compositions_2.append(res['compositions'])
        all_load_2.append(res['avg_track_load'])

    final_mean_2 = sum(all_results_2) / len(all_results_2)
    final_compositions_2 = sum(all_compositions_2) / len(all_results_2)
    final_load_2 = sum(all_load_2) / len(all_results_2)

    print(f"\nРезультаты для 2 веток:")
    print(f"  Среднее время пребывания вагона: {final_mean_2:.2f} ч")
    print(f"  Сформировано составов (ср.): {final_compositions_2:.0f}")
    print(f"  Загрузка веток: {final_load_2:.1f}%")


    print("\nЭксперимент 3: 3 ветки")

    N_opt_3, mean_3, sigma_3 = station_simulation.calculate_required_runs(3, 50, EPS, TA)

    all_results_3 = []
    all_compositions_3 = []
    all_load_3 = []

    for _ in range(max(N_opt_3, 10)):
        station = station_simulation.SortingStation(3)

        res = station.run()

        all_results_3.append(res['avg_residence_time'])
        all_compositions_3.append(res['compositions'])
        all_load_3.append(res['avg_track_load'])

    final_mean_3 = sum(all_results_3) / len(all_results_3)
    final_compositions_3 = sum(all_compositions_3) / len(all_results_3)
    final_load_3 = sum(all_load_3) / len(all_results_3)

    print(f"\nРезультаты для 3 веток:")
    print(f"  Среднее время пребывания вагона: {final_mean_3:.2f} ч")
    print(f"  Сформировано составов (ср.): {final_compositions_3:.0f}")
    print(f"  Загрузка веток: {final_load_3:.1f}%")


    print("Эксперимент 4: 4 ветки")
    N_opt_4, mean_4, sigma_4 = station_simulation.calculate_required_runs(4, 50, EPS, TA)

    all_results_4 = []
    all_compositions_4 = []
    all_load_4 = []
    for _ in range(max(N_opt_4, 10)):
        station = station_simulation.SortingStation(4)
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
    print(f"  Среднее время пребывания вагона: {final_mean_4:.2f} ч ({final_mean_4*60:.3f} мин)")
    print(f"  Всего обработано вагонов (ср.): {station.total_wagons}")
    print(f"  Сформировано составов (ср.): {final_compositions_4:.0f}")
    print(f"  Загрузка веток: {final_load_4:.1f}%")
    print(f"  СКО: {final_std_4:.4f} ч")
    print(f"  Относительная погрешность: {rel_error_4:.2f}%")


    print("Эксперимент 5: 5 веток")

    N_opt_5, mean_5, sigma_5 = station_simulation.calculate_required_runs(5, 50, EPS, TA)

    all_results_5 = []
    all_compositions_5 = []
    all_load_5 = []
    for _ in range(max(N_opt_5, 10)):
        station = station_simulation.SortingStation(5)
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
    print(f"  Среднее время пребывания вагона: {final_mean_5:.2f} ч ({final_mean_5*60:.3f} мин)")
    print(f"  Сформировано составов (ср.): {final_compositions_5:.0f}")
    print(f"  Загрузка веток: {final_load_5:.1f}%")
    print(f"  СКО: {final_std_5:.4f} ч")
    print(f"  Относительная погрешность: {rel_error_5:.2f}%")


    print("Эксперимент 6: 6 веток")
    N_opt_6, mean_6, sigma_6 = station_simulation.calculate_required_runs(6, 50, EPS, TA)

    all_results_6 = []
    all_compositions_6 = []
    all_load_6 = []

    for _ in range(max(N_opt_6, 10)):
        station = station_simulation.SortingStation(6)

        res = station.run()

        all_results_6.append(res['avg_residence_time'])
        all_compositions_6.append(res['compositions'])
        all_load_6.append(res['avg_track_load'])

    final_mean_6 = sum(all_results_6) / len(all_results_6)
    final_compositions_6 = sum(all_compositions_6) / len(all_compositions_6)
    final_load_6 = sum(all_load_6) / len(all_load_6)

    print(f"\nРезультаты для 6 веток:")
    print(f"  Среднее время пребывания вагона: {final_mean_6:.2f} ч ({final_mean_6*60:.3f} мин)")
    print(f"  Сформировано составов (ср.): {final_compositions_6:.0f}")
    print(f"  Загрузка веток: {final_load_6:.1f}%")


    print("\nЭксперимент 7: 7 веток")
    N_opt_7, mean_7, sigma_7 = station_simulation.calculate_required_runs(7, 50, EPS, TA)

    all_results_7 = []
    all_compositions_7 = []
    all_load_7 = []

    for _ in range(max(N_opt_7, 10)):
        station = station_simulation.SortingStation(7)

        res = station.run()

        all_results_7.append(res['avg_residence_time'])
        all_compositions_7.append(res['compositions'])
        all_load_7.append(res['avg_track_load'])

    final_mean_7 = sum(all_results_7) / len(all_results_7)
    final_compositions_7 = sum(all_compositions_7) / len(all_compositions_7)
    final_load_7 = sum(all_load_7) / len(all_load_7)

    print(f"\nРезультаты для 7 веток:")
    print(f"  Среднее время пребывания вагона: {final_mean_7:.2f} ч ({final_mean_7*60:.3f} мин)")
    print(f"  Сформировано составов (ср.): {final_compositions_7:.0f}")
    print(f"  Загрузка веток: {final_load_7:.1f}%")


    print("\nЭксперимент 8: 8 веток")
    N_opt_8, mean_8, sigma_8 = station_simulation.calculate_required_runs(8, 50, EPS, TA)

    all_results_8 = []
    all_compositions_8 = []
    all_load_8 = []

    for _ in range(max(N_opt_8, 10)):
        station = station_simulation.SortingStation(8)

        res = station.run()

        all_results_8.append(res['avg_residence_time'])
        all_compositions_8.append(res['compositions'])
        all_load_8.append(res['avg_track_load'])

    final_mean_8 = sum(all_results_8) / len(all_results_8)
    final_compositions_8 = sum(all_compositions_8) / len(all_results_8)
    final_load_8 = sum(all_load_8) / len(all_results_8)

    print(f"\nРезультаты для 8 веток:")
    print(f"  Среднее время пребывания вагона: {final_mean_8:.2f} ч ({final_mean_8*60:.3f} мин)")
    print(f"  Сформировано составов (ср.): {final_compositions_8:.0f}")
    print(f"  Загрузка веток: {final_load_8:.1f}%")


    print("\nЭксперимент 9: 9 веток")
    N_opt_9, mean_9, sigma_9 = station_simulation.calculate_required_runs(9, 50, EPS, TA)

    all_results_9 = []
    all_compositions_9 = []
    all_load_9 = []

    for _ in range(max(N_opt_9, 10)):
        station = station_simulation.SortingStation(9)

        res = station.run()

        all_results_9.append(res['avg_residence_time'])
        all_compositions_9.append(res['compositions'])
        all_load_9.append(res['avg_track_load'])

    final_mean_9 = sum(all_results_9) / len(all_results_9)
    final_compositions_9 = sum(all_compositions_9) / len(all_results_9)
    final_load_9 = sum(all_load_9) / len(all_results_9)

    print(f"\nРезультаты для 9 веток:")
    print(f"  Среднее время пребывания вагона: {final_mean_9:.2f} ч ({final_mean_9*60:.3f} мин)")
    print(f"  Сформировано составов (ср.): {final_compositions_9:.0f}")
    print(f"  Загрузка веток: {final_load_9:.1f}%")


    print("\nЭксперимент 10: 10 веток")

    N_opt_10, mean_10, sigma_10 = station_simulation.calculate_required_runs(10, 50, EPS, TA)

    all_results_10 = []
    all_compositions_10 = []
    all_load_10 = []

    for _ in range(max(N_opt_10, 10)):
        station = station_simulation.SortingStation(10)

        res = station.run()

        all_results_10.append(res['avg_residence_time'])
        all_compositions_10.append(res['compositions'])
        all_load_10.append(res['avg_track_load'])

    final_mean_10 = sum(all_results_10) / len(all_results_10)
    final_compositions_10 = sum(all_compositions_10) / len(all_results_10)
    final_load_10 = sum(all_load_10) / len(all_results_10)

    print(f"\nРезультаты для 10 веток:")
    print(f"  Среднее время пребывания вагона: {final_mean_10:.5f} ч ({final_mean_10*60:.3f} мин)")
    print(f"  Сформировано составов (ср.): {final_compositions_10:.0f}")
    print(f"  Загрузка веток: {final_load_10:.1f}%")



    tracks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    avg_times = [
        final_mean_1,
        final_mean_2,
        final_mean_3,
        final_mean_4,
        final_mean_5,
        final_mean_6,
        final_mean_7,
        final_mean_8,
        final_mean_9,
        final_mean_10
    ]

    plt.plot(tracks, avg_times, marker='o')

    plt.xlabel("Количество веток")
    plt.ylabel("Среднее время пребывания вагона, ч")
    plt.title("Зависимость времени пребывания от числа веток")

    plt.grid(True)

    plt.show()