from components.catcher import WebParser

class WebCatcher_4_Yande():
    def __init__(self,mode,key) -> None:
        self.status = None
        self.imgList = []
        self.previewList = []
        self.mode = mode
        # if search, and then imgList is a 2D list saving the imgList of each page
        self.pageList = []

        if mode == 'Popular':
            self.url = "https://yande.re/post/popular_recent?period=" + "1"+ key
        if mode == 'Search':
            self.baseurl2seg1 = "https://yande.re/post?page="
            baseurl2seg2 = "&tags="
            self.baseurl2seg2 = baseurl2seg2 + key
        self.WP = WebParser(self.url)

    def findImg(self):
        if self.mode == 'Popular':
            self.WP.askURL()
            self.WP.parser()
            self.WP.bsSelector("a[class='directlink largeimg']")
            for link in self.WP.selected_data:
                self.imgList.append(link.get('href'))
            self.status = self.WP.status
            self.WP.bsSelector("img[class='preview']")
            for link in self.WP.selected_data:
                self.previewList.append(link.get('src'))
            self.status = self.WP.status

    # def findPreview(self):
    #     if self.mode == 'Popular':
    #         self.WP.askURL()
    #         self.WP.parser()
    #         self.WP.bsSelector("img[class='preview']")
    #         for link in self.WP.selected_data:
    #             self.previewList.append(link.get('src'))
    #         self.status = self.WP.status

