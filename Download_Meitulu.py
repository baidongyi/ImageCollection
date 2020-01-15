from src.lib_share import *
import threading


def get_page_url_by_id(my_id) -> str:
    return 'https://www.meitulu.com/item/' + str(my_id) + '.html'


def get_img_url(my_id, img_num) -> str:
    return 'https://mtl.ttsqgs.com/images/img/' + str(my_id) + '//' + str(img_num) + '.jpg'


def save_image_by_id_num(img_id, img_num, bottom_folder) -> int:
    img_url = get_img_url(img_id, img_num)
    url_ref = get_page_url_by_id(img_id)

    file_path = os.path.join(bottom_folder, str(img_id) + '_' + str(img_num) + '.jpg')

    result = save_image_by_url_to_file(file_path, img_url, url_ref)

    # 0 for downloaded successfully , 1 for already exists, 2 for error 404 not found
    if result == 2:
        return 1
    elif result == 0:
        return 0
    else:
        return 0


def remove_char(title: str) -> str:
    my_list = '~!@#$%^&*()-+=\|;:/<>[]{}'
    for char in my_list:
        title = title.replace(char, '_')
    return title


def get_url_title(url) -> str:
    try:
        soup = get_soup_by_url(url)
    except:
        return '404'
    else:
        title = soup.find('h1').string
        wl('Get title:  ' + str(title), 2)
        return remove_char(title)


def is_img_id_exist(img_id: str, save_folder: str) -> bool:
    list_folder = os.listdir(save_folder)
    for one_folder in list_folder:
        if one_folder[0:len(img_id)] == img_id and one_folder[-7:] != 'working':
            return True
    return False


def save_image_by_id(img_id, save_folder):
    '''
    if is_img_id_exist(img_id, save_folder):
        wl(str(img_id) + ' Series => Already Exists', 1)
        return
    '''

    url = get_page_url_by_id(img_id)
    title = get_url_title(url)
    if title == '404':
        wl('ID: ' + str(img_id) + ' => invalid', 1)
        return

    wl(url, 3)

    bottom_folder = os.path.join(save_folder, str(img_id) + '_' + title)

    if not os.path.exists(bottom_folder):
        os.mkdir(bottom_folder)

    for img_num in range(1, 99):
        if save_image_by_id_num(img_id, img_num, bottom_folder) > 0:
            wl('reach Max =' + str(img_num), 1)
            break


def get_link_in_page(url: str) -> list:
    soup = get_soup_by_url(url)
    links = soup.find_all('a', attrs={"target": "_blank"})
    my_links = []
    for link in links:
        url_link = str(link.attrs['href'])
        if url_link.find('item') > 0:
            item = url_link.split('/')[4].replace('.html', '')
            my_links.append(item)
            wl('Get Item => ' + str(item), 3)
    return my_links


def get_link_by_name(name: str, page: int) -> list:
    if page > 1:
        url = 'https://www.meitulu.com/t/' + name + '/' + str(page) + '.html'
    else:
        url = 'https://www.meitulu.com/t/' + name

    wl('url => ' + url, 2)

    if get_url_title(url) == '404':
        wl('reach web limit count ', 1)
        return []
    else:
        return get_link_in_page(url)


def save_by_name(name: str, save_folder: str):
    for page in range(1, 999):
        my_links = get_link_by_name(name, page)
        if len(my_links) > 0:
            wl('Page ' + str(page) + ' have links count => ' + str(len(my_links)), 1)
            t_list = []
            for img_id in my_links:
                t = threading.Thread(target=save_image_by_id, args=(img_id, save_folder))
                t.start()
                t_list.append(t)

            for t in t_list:
                t.join()
        else:
            return


def main():
    base_folder = os.path.join(get_base_folder(), 'meitulu')

    name_list = ['1384']

    for name in name_list:
        save_by_name(name, base_folder)


if __name__ == '__main__':
    main()
