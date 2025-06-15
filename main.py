import tkinter as tk
import pygame
import time
from functools import partial
import threading

# pip freeze > requirements.txt





import os

# Укажите путь к папке
folder_path = 'audio'

# Получить список файлов и папок в папке
files = os.listdir(folder_path)



l = []
for i in files:
    l.append(i[0:5]+"\n"+i[5:15])







btn = {}

b_place = [
[50, 50],
[150, 50],
[250, 50],
[350, 50],
[450, 50],

[50, 150],
[150, 150],
[250, 150],
[350, 150],
[450, 150],


[50, 250],
[150, 250],
[250, 250],
[350, 250],
[450, 250],


[50, 350],
[150, 350],
[250, 350],
[350, 350],
[450, 350],


[50, 450],
[150, 450],
[250, 450],
[350, 450],
[450, 450],

]




window = tk.Tk()
pygame.mixer.init()





class A:
    volume = 1
    current_time = 0  # в секундах
    is_playing = False
    update_thread = None
    paused = False
    music_length = 0
    musictime = 0
    new_pos = 0
    music_time_save = 0






# переводит в нужный формат время
def format_time(seconds):
    minutes = int(seconds // 60)
    sec = int(seconds % 60)
    return f"{minutes:02d}:{sec:02d}"




# обновляет счетчик времени на экране и ползунке
def update_labels():
    if A.current_time > A.music_length:
        time = A.music_length
    else:
        time = A.current_time

    time_label.config(text=f"{format_time(time)} / {format_time(A.music_length)}")
    a = ((A.current_time) * 100) / A.music_length
    scale.set(a)






# старт воспроизведения
def start_playback():
    seek(A.current_time)
    A.is_playing = True



# старт воспроизведения
def start_playback1(arg):
    A.music_length = pygame.mixer.Sound(f"audio/{arg}").get_length()
    pygame.mixer.music.load(f"audio/{arg}")
    pygame.mixer.music.play(start=0)
    A.music_time_save = 0
    A.new_pos = 0
    A.is_playing = True
    A.paused = True




    # Запускаем поток для обновления времени
    def update_time():
        while True:
            time.sleep(0.01)
            musictime = pygame.mixer.music.get_pos() / 1000
            if musictime >= 0:
                A.musictime = musictime
            else:
                A.musictime = 0


            if A.musictime>0:
                A.current_time = A.musictime + A.new_pos + A.music_time_save
            # print(A.current_time, A.musictime, A.new_pos)

            # if A.current_time >= A.music_length:
            #     A.current_time = A.music_length
            #     break

            update_labels()

    update_thread = threading.Thread(target=update_time, daemon=True)
    update_thread.start()











# пауза воспроизведения
def stop_playback():
    A.music_time_save = A.musictime + A.music_time_save
    pygame.mixer.music.stop()
    A.is_playing = False





# запускает перемотку по position
def seek(position):
    if 0 <= position <= A.music_length:
        A.current_time = position
        pygame.mixer.music.play(start=A.current_time)










# перемотка на 5 секунд вперед
def move_forward(event):
    step = 5  # перемотка на 5 секунд вперед

    new_pos = A.current_time + step
    if new_pos > A.music_length:
        A.new_pos = A.music_length
    else:
        A.new_pos = new_pos
    seek(A.new_pos)
    update_labels()







# перемотка назад на 5 секунд
def move_backward(event):
    step = 5  # перемотка назад на 5 секунд
    new_pos = A.current_time - step
    if new_pos < 0:
        A.new_pos = 0
    else:
        A.new_pos = new_pos
    seek(A.new_pos)
    update_labels()












def pause_resume(event=None):
    if A.paused == True:
        if A.is_playing:
            stop_playback()
        else:
            start_playback()







# Кнопка плавное затухание звука
def sound_down():
    for i in range(100, 9, -1):
        pygame.mixer.music.set_volume(i/100)
        scale1.set(i)
        time.sleep(0.009)



# Кнопка плавное возвращение звука до 100
def sound_up():
    for i in range(10, 101):
        pygame.mixer.music.set_volume(i/100)
        scale1.set(i)
        time.sleep(0.009)



pygame.mixer.music.set_volume(A.volume)






























# создание 16 кнопок для запуска дорожек
for i in range(len(l)):
    btn[i] = tk.Button(window, text=l[i], width=10, height=3, command=partial(start_playback1, files[i]))
    # btn[i] = tk.Button(window, text=f"Фоногр. {i+1}", width=10, height=3, command=start_playback1)
    btn[i].place(x=b_place[i][0], y=b_place[i][1])




# Метка для отображения времени
time_label = tk.Label(window, text="00:00 / 00:00")
time_label.place(x=253, y=610)

# Кнопка для запуска дорожки
start_button = tk.Button(window, text="Старт", command=start_playback)
start_button.place(x=293, y=550)

# Кнопка для остановки дорожки
stop_button = tk.Button(window, text="Пауза", command=stop_playback)
stop_button.place(x=243, y=550)


# Кнопка плавное затухание звука
sound_down_b = tk.Button(window, text="down", command=sound_down)
sound_down_b.place(x=500, y=600)


# Кнопка плавное возвращение звука до 100
sound_up_b = tk.Button(window, text="up", command=sound_up)
sound_up_b.place(x=500, y=550)




# функция изменения звука роликом мыши
def change_volume(event):
    # print(event)
    # event.delta > 0 при прокрутке вверх, < 0 при вниз
    if event.delta > 0:
        A.volume = min(A.volume + 0.05, 1.0)
    else:
        A.volume = max(A.volume - 0.05, 0.0)
    pygame.mixer.music.set_volume(A.volume)
    scale1.set(A.volume*100)
    # print(f"Громкость: {A.volume:.2f}")







# функция изменения звука ползунком
def change_volume1(event):
    pygame.mixer.music.set_volume(float(event)/100)
    A.volume = float(event)/100




# функция промотки ползунком
def change_volume2(event):
    pass
    # print(event, A.music_length, A.current_time)
    # b = (int(event)*A.music_length)/100
    #
    # print(A.current_time, b)
    # a = (A.current_time * 100) / A.music_length
    # print(event, A.current_time, int(a))








# Ползунок аудиодорожка
scale = tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, command=change_volume2, width=10, length=480)
scale.set(0)  # Начальное значение
scale.pack(pady=10)
scale.place(x=50, y=650)





# Ползунок звука
scale1 = tk.Scale(window, from_=100, to=0, orient=tk.VERTICAL, command=change_volume1, width=10, length=80)
scale1.set(100)  # Начальное значение громкости
scale1.pack(pady=20)
scale1.place(x=450, y=550)









# <Связываем стрелки с функциями перемотки>
window.bind('<Left>', move_backward)
window.bind('<Right>', move_forward)
window.bind('<space>', pause_resume)

# Обработка события прокрутки мыши для всего окна
window.bind("<MouseWheel>", change_volume)





window.title("Фонограммы Последний шанс")
window.geometry('580x700')
window.mainloop()









