import matplotlib.pyplot as plt
import numpy as np


def plot():
    """Plot random vs norm vs sim vs dis
    """
    ratio = np.around(np.arange(0.05, 0.96, 0.05), 2)
    
    pruned_acc_dict = {
        'random': [90.11, 82.59, 58.23, 25.19, 18.02, 10.84, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
        'L0_norm': [91.59, 87.58, 61.16, 34.15, 17.23, 10.66, 10.01, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
        'L1_norm': [91.84, 83.56, 71.48, 47.84, 33.3, 25.21, 15.62, 11.04, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
        'L2_norm': [91.82, 84.24, 70.12, 51.9, 38.98, 28.33, 17.64, 12.8, 10.11, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
        'inf_norm': [92.56, 87.97, 79.28, 62.8, 53.73, 41.68, 20.7, 14.49, 10.09, 10.0, 10.01, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
        'cosine_sim': [88.12, 69.17, 59.78, 37.9, 26.54, 22.28, 11.78, 10.05, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
        'Pearson_sim': [87.43, 68.94, 42.13, 27.35, 17.61, 14.12, 10.17, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
        'Euclide_dis': [91.18, 85.58, 71.26, 53.6, 44.84, 31.91, 22.96, 13.63, 10.02, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
        'Manhattan_dis': [91.07, 84.25, 71.99, 52.68, 41.86, 32.81, 18.86, 10.82, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
        'SNR_dis': [81.13, 58.27, 21.08, 15.51, 11.48, 13.52, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0]
        }

    finetuned_acc_dict = {
        'random': [93.11, 92.95, 92.4, 92.31, 91.5, 91.73, 90.82, 89.82, 89.35, 87.47, 86.86, 83.37, 80.85, 77.15, 73.1, 69.48, 61.29, 57.07, 10.0],
        'L0_norm': [93.22, 93.03, 92.59, 92.32, 91.87, 91.22, 91.01, 89.9, 88.98, 88.31, 86.61, 84.66, 84.02, 77.5, 74.64, 73.41, 67.31, 43.2, 10.0],
        'L1_norm': [93.48, 93.06, 92.93, 92.62, 92.21, 91.71, 91.3, 90.86, 90.09, 89.29, 88.65, 87.43, 84.46, 78.94, 76.48, 65.75, 65.77, 55.63, 44.74],
        'L2_norm': [93.44, 92.94, 92.8, 92.49, 92.31, 91.78, 91.54, 91.16, 90.41, 89.25, 89.21, 87.43, 84.86, 75.98, 66.78, 58.29, 60.01, 52.65, 39.19],
        'inf_norm': [93.3, 93.18, 92.95, 92.48, 92.0, 91.92, 91.35, 90.16, 89.97, 88.64, 87.92, 86.28, 79.63, 76.13, 62.66, 66.69, 62.42, 47.85, 10.0],
        'cosine_sim': [93.37, 92.89, 92.61, 92.31, 91.76, 91.07, 90.72, 90.13, 88.67, 86.84, 78.04, 72.46, 71.4, 67.69, 64.33, 66.36, 61.51, 51.41, 37.8],
        'Pearson_sim': [93.44, 92.9, 92.59, 91.79, 91.62, 90.98, 90.63, 89.44, 88.12, 86.71, 83.78, 70.38, 69.16, 66.7, 63.13, 66.2, 58.95, 53.51, 38.95],
        'Euclide_dis': [93.36, 93.19, 92.87, 92.89, 92.4, 91.97, 91.37, 90.66, 90.55, 89.55, 88.73, 87.05, 84.16, 71.52, 64.95, 62.45, 57.95, 48.04, 47.87],
        'Manhattan_dis': [93.44, 93.31, 93.09, 92.52, 92.44, 91.94, 90.97, 91.36, 90.23, 89.48, 88.76, 86.87, 84.85, 81.1, 75.86, 61.69, 59.29, 51.04, 42.84],
        'SNR_dis': [93.02, 92.81, 91.84, 91.58, 90.61, 89.58, 89.05, 87.05, 86.05, 84.75, 84.7, 82.17, 76.89, 70.41, 68.79, 65.48, 57.69, 45.06, 10.0]
        }

    plt.figure(dpi=1200)
    fig, axis = plt.subplots(1, 2)

    for k, v in pruned_acc_dict.items():        
        axis[0].plot(ratio, v, label=k)
    axis[0].set_title("pruned")
    axis[0].legend()

    for k, v in finetuned_acc_dict.items():
        axis[1].plot(ratio, v, label=k)
    axis[1].set_title("finetuned")
    axis[1].legend()

    plt.xlabel('ratio')
    plt.ylabel('accuracy')
    plt.savefig('plot.png', dpi = 1200)


def plot_comparision():
    """Plot sum vs min_min vs min_sum
    """
    min_sum_dict = {'cosine_sim': [92.91, 92.43, 91.93, 90.22, 89.05, 88.5, 87.81, 85.65, 81.3, 76.64, 75.95, 70.51, 64.76, 56.43, 60.77, 57.26, 56.6, 49.07, 47.93, 39.09, 36.49, 33.76, 31.37, 33.18, 26.79, 22.75, 22.61, 23.08, 19.37, 15.63, 12.73, 12.21, 11.65, 12.43, 12.36, 11.15, 10.32, 10.05, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0], 'Pearson_sim': [93.0, 92.42, 91.62, 90.92, 89.5, 89.49, 88.02, 86.15, 80.69, 78.73, 75.5, 65.5, 64.26, 58.57, 62.34, 57.23, 56.69, 50.83, 46.61, 43.96, 43.05, 38.63, 33.48, 31.11, 28.36, 20.62, 19.99, 20.6, 18.12, 18.02, 19.25, 18.71, 18.05, 12.13, 14.25, 15.09, 12.19, 15.09, 11.62, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0], 'Euclide_dis': [93.2, 92.4, 91.86, 91.55, 91.22, 90.35, 88.98, 86.7, 84.98, 84.11, 83.52, 82.91, 78.4, 75.55, 70.3, 67.06, 62.22, 57.92, 57.86, 53.42, 51.47, 49.94, 47.91, 44.22, 39.11, 37.18, 33.57, 30.67, 26.46, 23.25, 19.64, 18.32, 17.51, 15.21, 13.71, 11.78, 10.77, 10.29, 10.12, 10.04, 10.03, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0], 'Manhattan_dis': [93.13, 92.49, 92.0, 91.55, 90.93, 90.4, 89.38, 87.16, 85.73, 84.13, 83.06, 80.21, 77.48, 74.05, 72.73, 69.02, 64.27, 60.6, 59.32, 57.76, 54.02, 52.47, 46.83, 41.7, 36.04, 34.77, 32.81, 30.0, 29.12, 27.62, 24.11, 22.35, 19.37, 17.61, 16.88, 14.45, 13.12, 12.63, 11.24, 10.76, 10.26, 10.08, 10.04, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0]}
    min_min_dict = {'cosine_sim': [93.02, 92.39, 91.81, 90.13, 89.68, 88.51, 87.78, 85.55, 81.65, 80.3, 80.12, 73.59, 70.16, 63.36, 54.73, 51.69, 50.36, 45.99, 40.62, 40.73, 33.41, 28.76, 30.42, 28.43, 25.71, 23.25, 21.64, 20.26, 18.14, 17.05, 16.43, 16.35, 14.61, 11.85, 11.56, 14.1, 12.79, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0], 'Pearson_sim': [93.05, 92.31, 91.49, 90.54, 89.85, 89.03, 87.86, 85.75, 82.38, 80.77, 76.9, 70.09, 68.58, 62.3, 51.48, 47.84, 42.01, 40.31, 38.06, 35.15, 33.57, 29.93, 24.83, 21.95, 23.43, 21.11, 21.21, 18.93, 17.19, 16.27, 16.17, 16.51, 14.4, 13.64, 11.04, 11.78, 11.74, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0], 'Euclide_dis': [93.13, 92.38, 92.4, 91.67, 91.13, 89.55, 88.35, 87.62, 84.91, 82.75, 82.67, 80.41, 77.71, 71.01, 69.31, 65.86, 63.84, 61.25, 55.09, 50.07, 47.96, 45.08, 42.58, 38.31, 33.32, 29.7, 26.15, 24.35, 20.77, 19.06, 16.9, 16.27, 15.11, 13.2, 13.2, 12.43, 10.88, 10.5, 10.2, 10.08, 10.01, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0], 'Manhattan_dis': [93.04, 92.61, 92.24, 91.76, 91.19, 89.17, 88.43, 87.74, 84.69, 81.5, 76.56, 74.69, 72.72, 70.12, 66.83, 63.34, 61.31, 59.25, 55.02, 51.36, 47.86, 44.85, 41.27, 38.78, 36.92, 33.14, 32.32, 30.45, 26.84, 24.0, 20.26, 18.9, 18.32, 16.86, 15.45, 13.4, 12.05, 11.48, 10.38, 10.05, 10.03, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0]}
    sum_dict = {'cosine_sim': [93.02, 92.41, 90.67, 89.17, 88.12, 82.16, 79.15, 71.51, 71.5, 69.17, 62.74, 69.28, 65.0, 60.4, 59.78, 57.39, 51.25, 47.73, 44.76, 37.9, 35.25, 31.74, 28.4, 24.73, 26.54, 25.36, 24.23, 23.83, 21.45, 22.28, 22.31, 16.47, 15.26, 12.85, 11.78, 11.01, 10.23, 10.14, 10.07, 10.05, 10.03, 9.99, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0], 'Pearson_sim': [92.64, 91.44, 90.05, 87.71, 87.43, 85.0, 82.29, 79.22, 69.58, 68.94, 65.85, 60.18, 56.06, 50.21, 42.13, 40.68, 35.89, 32.86, 30.08, 27.35, 26.65, 24.67, 22.75, 20.57, 17.61, 15.46, 16.93, 15.2, 12.8, 14.12, 11.77, 10.91, 10.41, 10.21, 10.17, 10.23, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 9.99, 10.0, 10.0], 'Euclide_dis': [93.26, 93.16, 92.33, 91.81, 91.18, 90.6, 89.43, 89.27, 87.35, 85.58, 84.11, 81.95, 77.83, 75.76, 71.26, 66.43, 61.31, 57.98, 57.13, 53.6, 52.15, 49.95, 48.76, 46.58, 44.84, 43.88, 40.99, 39.61, 35.95, 31.91, 31.22, 29.35, 27.01, 24.67, 22.96, 19.86, 18.02, 16.84, 16.1, 13.63, 12.1, 10.86, 10.6, 10.16, 10.02, 10.01, 10.01, 10.0, 10.0, 10.0], 'Manhattan_dis': [93.42, 93.16, 92.49, 91.49, 91.07, 89.85, 89.17, 87.47, 86.13, 84.25, 83.86, 82.55, 79.18, 77.05, 71.99, 68.08, 60.99, 60.39, 57.48, 52.68, 50.19, 48.67, 43.38, 42.21, 41.86, 39.5, 38.14, 35.26, 35.12, 32.81, 28.9, 26.7, 24.13, 21.99, 18.86, 16.86, 15.08, 13.64, 12.27, 10.82, 10.45, 10.15, 10.1, 10.01, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0]}
    ratio = np.around(np.arange(0.01, 0.51, 0.01), 2)

    cosine_sim_dict = {
        'min_sum': min_sum_dict['cosine_sim'],
        'min_min': min_min_dict['cosine_sim'],
        'sum': sum_dict['cosine_sim']
        }

    Pearson_sim_dict = {
        'min_sum': min_sum_dict['Pearson_sim'],
        'min_min': min_min_dict['Pearson_sim'],
        'sum': sum_dict['Pearson_sim']
        }

    Euclide_dis_dict = {
        'min_sum': min_sum_dict['Euclide_dis'],
        'min_min': min_min_dict['Euclide_dis'],
        'sum': sum_dict['Euclide_dis']
        }

    Manhattan_dis_dict = {
        'min_sum': min_sum_dict['Manhattan_dis'],
        'min_min': min_min_dict['Manhattan_dis'],
        'sum': sum_dict['Manhattan_dis']
        }

    plt.figure(dpi=1200)
    fig, axis = plt.subplots(2, 2)

    for k, v in cosine_sim_dict.items():        
        axis[0, 0].plot(ratio, v, label=k)
    axis[0, 0].set_title("cosine_sim")
    axis[0, 0].legend()

    for k, v in Pearson_sim_dict.items():
        axis[0, 1].plot(ratio, v, label=k)
    axis[0, 1].set_title("Pearson_sim")
    axis[0, 1].legend()

    for k, v in Euclide_dis_dict.items():
        axis[1, 0].plot(ratio, v, label=k)
    axis[1, 0].set_title("Euclide_dis")
    axis[1, 0].legend()

    for k, v in Manhattan_dis_dict.items():        
        axis[1, 1].plot(ratio, v, label=k)
    axis[1, 1].set_title("Manhattan_dis")
    axis[1, 1].legend()

    plt.xlabel('ratio')
    plt.ylabel('accuracy')
    plt.savefig('compare_01.png', dpi = 1200)


    '''
    #sum vs min_min vs min_sum in range [0.05, 0.95, step=0.05]
    ratio = np.around(np.arange(0.05, 0.96, 0.05), 2)
    cosine_sim_dict = {
        'min_sum': [89.05, 76.64, 60.77, 39.09, 26.79, 15.63, 12.36, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
        'min_min': [89.68, 80.3, 54.73, 40.73, 25.71, 17.05, 11.56, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
        'cosine_sim': [88.12, 69.17, 59.78, 37.9, 26.54, 22.28, 11.78, 10.05, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
        }

    Pearson_sim_dict = {
        'min_sum': [89.5, 78.73, 62.34, 43.96, 28.36, 18.02, 14.25, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
        'min_min': [89.85, 80.77, 51.48, 35.15, 23.43, 16.27, 11.04, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
        'Pearson_sim': [87.43, 68.94, 42.13, 27.35, 17.61, 14.12, 10.17, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0]
        }

    Euclide_dis_dict = {
        'min_sum': [91.22, 84.11, 70.3, 53.42, 39.11, 23.25, 13.71, 10.04, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
        'min_min': [91.13, 82.75, 69.31, 50.07, 33.32, 19.06, 13.2, 10.08, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
        'Euclide_dis': [91.18, 85.58, 71.26, 53.6, 44.84, 31.91, 22.96, 13.63, 10.02, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
        }

    Manhattan_dis_dict = {
        'min_sum': [90.93, 84.13, 72.73, 57.76, 36.04, 27.62, 16.88, 10.76, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
        'min_min': [91.19, 81.5, 66.83, 51.36, 36.92, 24.0, 15.45, 10.05, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
        'Manhattan_dis': [91.07, 84.25, 71.99, 52.68, 41.86, 32.81, 18.86, 10.82, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
        }
    '''


plot_comparision()
