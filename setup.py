from jcrawler_comments.wyycomment import main


def whether_use_proxy(whether=None):
    """
    :param whether: 是否使用代理ip
    :return:
    """
    if whether:
        main(wetherProxie=True)
    else:
        main()

if __name__ == '__main__':

    whether_use_proxy()