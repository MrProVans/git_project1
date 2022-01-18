import pygame
from random import choice, shuffle
from time import time, sleep

screen_color = (255, 255, 150)
task_color = (0, 17, 142)
answers_color = (0, 17, 142)
score_color = (255, 17, 142)
score = 0
sleep_time = 0.5  # Время ожидания.
min_number = 11
max_number = 99

if max_number < 100:
    x_task_left = 260
    x_task_right = 400
elif max_number < 1000:
    x_task_left = 230
    x_task_right = 420
elif max_number < 10000:
    x_task_left = 230
    x_task_right = 450
else:
    x_task_left = 160
    x_task_right = 500


def change(df_digit, zero_key=False):
    if zero_key:
        result = [0]
    else:
        result = []
    if df_digit == 0:
        result.extend([1, 2, 3])
    elif df_digit == 1:
        result.extend([2, 3, 4])
    elif df_digit == 2:
        result.extend([1, 3, 4])
    elif df_digit == 3:
        result.extend([1, 2, 4])
    elif df_digit == 9:
        result.extend([6, 7, 8])
    elif df_digit == 8:
        result.extend([6, 9, 9])
    elif df_digit == 7:
        result.extend([6, 8, 9])
    else:
        result.extend([df_digit - 2, df_digit - 1, df_digit + 1, df_digit + 2])
    return result


def making_up_answers(df_answer):
    result = []
    df_answer = str(df_answer)
    if len(df_answer) == 2:
        first_d = int(df_answer[0])


def making_task(a=11, b=99):  # Создание примера.
    x = choice(list(range(a, b + 1)))
    y = choice(list(range(a, b + 1)))
    answer = x * y
    #  summand = choice(list(range(1, 21)))
    wrong_answers_list = []
    # for df_i in range(1, 50, 1):
    #     wrong_answers_list.append(answer - df_i * summand)
    #     wrong_answers_list.append(answer + df_i * summand)
    for df_i in [-10, 10, -20, 20, -30, 30, -100, 100, -200, 200, -300, 300]:
        wrong_answers_list.append(answer - df_i)
        wrong_answers_list.append(answer + df_i)

    shuffle(wrong_answers_list)
    last_digit = str(answer)[- 1]
    wrong_answers_list = [str(number)[0:- 1] + last_digit for number in wrong_answers_list]
    wrong_answers_list = delete_duplicates(wrong_answers_list)
    df_answers_list = wrong_answers_list[0:3]
    df_answers_list.append(answer)
    shuffle(df_answers_list)
    df_this_task = f"{x} x {y} =?"
    df_true_index = df_answers_list.index(answer)
    if len(delete_duplicates(df_answers_list)) != 4:
        print('Ошибка!')
        print(df_answers_list)
    df_answers_list = [str(number) for number in df_answers_list]
    return [df_this_task, df_answers_list, df_true_index]


def draw_task(df_this_task, df_answers_list, df_score):
    draw(screen, df_this_task, 300, 200, task_color)
    df_ans1 = draw(screen, df_answers_list[0], x_task_left, 300, answers_color)
    df_ans2 = draw(screen, df_answers_list[1], x_task_left, 360, answers_color)
    df_ans3 = draw(screen, df_answers_list[2], x_task_right, 300, answers_color)
    df_ans4 = draw(screen, df_answers_list[3], x_task_right, 360, answers_color)
    draw(screen, f"Ваши очки: {round(df_score, 4)}", 200, 500, score_color)
    pygame.display.flip()
    df_start_time = time()
    return [df_ans1, df_ans2, df_ans3, df_ans4, df_start_time]


def counting_score(t, k=3):
    return 8 / t ** k


def counting_lower_score(this_score, k=3):
    return this_score ** (1 / k)


def delete_duplicates(this_list):
    new_list = []
    for element in this_list:
        if element not in new_list:
            new_list.append(element)
    return new_list


def draw(screen1, task, text_x, text_y, color, frame_color=(62, 0, 255), font=50, frame=True):
    font = pygame.font.Font(None, font)
    text = font.render(task, True, color)
    text_w = text.get_width()
    text_h = text.get_height()
    screen1.blit(text, (text_x, text_y))
    if frame:
        pygame.draw.rect(screen1, frame_color, (text_x - 10, text_y - 10,
                                                text_w + 20, text_h + 20), 3)
    return [text_x - 10, text_x - 10 + text_w + 20, text_y - 10, text_y - 10 + text_h + 20]


def light_frame(screen1, coord, frame_color):
    pygame.draw.rect(screen1, frame_color, (coord[0], coord[2],
                                            coord[1] - coord[0], coord[3] - coord[2]), 3)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    screen.fill(screen_color)
    pygame.display.flip()
    running = True
    start = True
    while running:
        for event in pygame.event.get():
            continue_key = False
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                if not start:
                    key = True
                    for i in range(4):
                        if ans_pos[i][0] <= event.pos[0] <= ans_pos[i][1] and ans_pos[i][2] <= event.pos[1] <= ans_pos[i][3]:
                            light_frame(screen, ans_pos[i], (0, 255, 0))
                            key = False
                            break
                    if key:
                        for i in range(4):
                            light_frame(screen, ans_pos[i], answers_color)
                    pygame.display.flip()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(4):
                    if ans_pos[i][0] <= event.pos[0] <= ans_pos[i][1] and\
                       ans_pos[i][2] <= event.pos[1] <= ans_pos[i][3]:
                        if true_index == i:
                            score += counting_score(time() - st_time, 3)
                            print('Верно!')
                            draw(screen, 'Верно!', 50, 20, score_color, font=100, frame=False)
                        else:
                            score = counting_lower_score(score)
                            print('Неверно!')
                            draw(screen, 'Неверно!', 50, 20, score_color, font=100, frame=False)
                        pygame.display.flip()
                        sleep(sleep_time)
                        break
                else:
                    print('Нажата не кнопка.')
                    continue_key = True
            elif not start:
                continue
            if continue_key:
                continue
            screen.fill(screen_color)
            [this_task, answers_list, true_index] = making_task(min_number, max_number)
            result_draw = draw_task(this_task, answers_list, score)
            st_time = result_draw[- 1]
            ans_pos = result_draw[0:4]
            pygame.display.flip()
            true_answer = False
            start = False
    pygame.quit()
