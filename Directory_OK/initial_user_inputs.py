# Data entry block
for_ok_input = input(
    'Введите через пробел id пользователя (или никнейм) и кол-во фотографий, нужных вам. '
    'Затем нажмите Enter. \nВнимание! Сервис может выдать меньшее кол-во фото, чем вы запрашиваете.\n'
    'Итак, введите через пробел id и кол-во фото : ').split(
    ' ')  # use for example: 576339763099 4 # or peftiev 3

folder_input = input('\nВведите название папки, которая будет располагаться на Яндекс.Диске,\n'
                     'в которую затем будут загружены фотки из соцсетей. Внимание! Если вы\n'
                     'введете название папки, которая уже существует на Я.Диске, то фото будут загружены\n'
                     'в существующую папку. Итак, введите название папки : ')  # use for example: My_new_folder

json_input = (
    input(
        '\nВведите название json-файла (без ковычек и расширения), он автоматически создастся,'
        '\nи в него будем записывать данные о фото. Внимание! Если вы введете название уже\n'
        'существующего json-файла, то этот файл полностью перезапишется. Итак, ведите название json-файла: '))