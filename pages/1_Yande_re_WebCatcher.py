
from components.yande import WebCatcher_4_Yande
import streamlit as st
import time
import wget
import os
import json

class ImageSaver():
    def __init__(self) -> None:
        # read the config file
        with open('config.json','r') as f:
            config = json.load(f)["yande_re"]
        self.manual_path = config["manual_folder_path"]
        self.auto_path_d = config["auto_folder_path_d"]
        self.auto_path_w = config["auto_folder_path_w"]
        self.auto_path_m = config["auto_folder_path_m"]
        self.auto_path_y = config["auto_folder_path_y"]

    def manual_save(self, url: str, name=None) -> None:
        if not os.path.exists(self.manual_path):
            os.mkdir(self.manual_path)
        # keep default name in wget
        # os.system(f"wget --content-disposition {url}")
        filepath = os.path.join(self.manual_path, name + '.jpg') if name else self.manual_path

        # Construct the wget command with the -N option
        command = ['wget', '--timestamping', '-P', filepath, url]

        # Execute the wget command
        os.system(' '.join(command))

    def auto_save(self, key, url: list, name=None) -> None:
        import time
        key = key[0].lower()
        if key == 'd':
            path = self.auto_path_d
        if key == 'w':
            path = self.auto_path_w
        if key == 'm':
            path = self.auto_path_m
        if key == 'y':
            path = self.auto_path_y
        if not os.path.exists(path):
            os.mkdir(path)
        # popular_d_2024-02-03
        time = time.strftime("%Y-%m-%d", time.localtime())
        dir_name = "popular_" + key + '_' + time
        dir_path = os.path.join(path,dir_name)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        # keep default name in wget
        # os.system(f"wget --content-disposition {url}")
        with st.status("Downloading...") as status:
            for i in range(len(url)):

                filepath = os.path.join(dir_path, name[i] + '.jpg') if name else dir_path

                # Construct the wget command with the -N option
                command = ['wget', '--timestamping', '-P', filepath, url[i]]

                # Execute the wget command
                os.system(' '.join(command))
                # write the download status
                st.write(f"Downloaded {i+1}/{len(url)}")
            status.update(label="Download complete!", state="complete", expanded=False)
        
        


ImageSaver = ImageSaver()
changed = False
st.sidebar.header("Mode")
mode = st.sidebar.radio("Select the mode", ["Popular", "Search"])

# save the session state mode(update immediately)
if 'mode' not in st.session_state:
    st.session_state['mode'] = mode
    changed = True
if st.session_state['mode'] != mode:
    st.session_state['mode'] = mode
    changed = True

if mode == 'Popular':
    st.sidebar.header("Period")
    key = st.sidebar.radio("Select the time", ["Day", "Week", "Month", "Year"])
    # set session state key(update immediately)
    if 'key' not in st.session_state:
        st.session_state['key'] = key
        changed = True
    if st.session_state['key'] != key:
        st.session_state['key'] = key
        changed = True

    st.header(" Popular Images of the " + key) 
    
    key = key[0].lower()
    # fetch the image list when session state is updated
    if changed:
        W4Y = WebCatcher_4_Yande(mode,key)
        W4Y.findImg()
        st.toast(':green[Image List load successfully!]', icon='🎉')
        # save the session state
        st.session_state['imgList'] = W4Y.imgList
        st.session_state['status'] = W4Y.status
        st.session_state['previewList'] = W4Y.previewList
    
    date, pre ,showAll,downloadAll = st.columns(4)
    with date:
        st.write(time.strftime("%Y-%m-%d", time.localtime()))
    with pre:
        isPreview = st.toggle("Preview", value=True)
    with showAll:
        isShowAll = st.toggle("Show All", value=False)

    if st.session_state['status'] == 200:
        if not isPreview:
            x = st.slider("Select a value", 1, len(st.session_state['imgList']))
            # st.write(st.session_state['imgList'][x-1])
            if os.path.exists('temp.jpg'):
                os.remove('temp.jpg')
            wget.download(st.session_state['imgList'][x-1], 'temp.jpg')
            st.image('temp.jpg', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
        if isPreview:
            if not isShowAll:
                x = st.slider("Select a value", 1, len(st.session_state['previewList']))
                # st.write(st.session_state['previewList'][x-1])
                if os.path.exists('single_temp'):
                    os.system('rm -r single_temp')
                os.mkdir('single_temp')
                wget.download(st.session_state['previewList'][x-1], 'single_temp/temp.jpg')
                lb,cb,rb = st.columns([0.5,0.25,0.25])
                with lb:
                    st.image('single_temp/temp.jpg', caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
                with cb:
                    st.link_button("Original",url=st.session_state['imgList'][x-1])
                with rb:
                    st.button("Download",key = x, on_click=lambda args: ImageSaver.manual_save(st.session_state['imgList'][args-1]), args=[x])
            if isShowAll:
                # generate the download all button if show all is selected
                with downloadAll:
                    st.button("Download All",key = 'd', on_click=lambda: ImageSaver.auto_save(st.session_state['key'],st.session_state['imgList']))
                # remove the temp folder
                if changed:
                    if os.path.exists('temp'):
                        os.system('rm -r temp')
                    os.mkdir('temp')

                count = 0
                for i in range(1,len(st.session_state['previewList'])):
                    url = st.session_state['imgList'][i-1]

                    # download the image to the temp folder
                    if changed:
                        wget.download(st.session_state['previewList'][i-1], 'temp/'+str(i)+'.jpg')
                    
                    if count == 0:
                        l,c,r = st.columns(3)
                    if count == 0:
                        with l:
                            st.image('temp/'+str(i)+'.jpg', caption=None, width=None, use_column_width=None, clamp=True, channels="RGB", output_format="auto")
                            lb,rb = st.columns(2)
                            with lb:
                                st.link_button("Original",url=st.session_state['imgList'][i-1])
                            with rb:
                                st.button("Download",key = i, on_click=lambda args: ImageSaver.manual_save(st.session_state['imgList'][args-1]), args=[i])
                    if count == 1:
                        with c:
                            st.image('temp/'+str(i)+'.jpg', caption=None, width=None, use_column_width=None, clamp=True, channels="RGB", output_format="auto")
                            lb,rb = st.columns(2)
                            with lb:
                                st.link_button("Original",url=st.session_state['imgList'][i-1])
                            with rb:
                                st.button("Download",key = i, on_click=lambda args: ImageSaver.manual_save(st.session_state['imgList'][args-1]), args=[i])
                    if count == 2:
                        with r:
                            st.image('temp/'+str(i)+'.jpg', caption=None, width=None, use_column_width=None, clamp=True, channels="RGB", output_format="auto")
                            lb,rb = st.columns(2)
                            with lb:
                                st.link_button("Original",url=st.session_state['imgList'][i-1])
                            with rb:
                                st.button("Download",key = i, on_click=lambda args: ImageSaver.manual_save(st.session_state['imgList'][args-1]), args=[i])
                    count = (count + 1)%3
                


    else:
        st.error("Image List load failed 😢")
        st.write(W4Y.status)


    



if mode == 'Search':
    key = st.sidebar.text_input("Enter the key")
    key = key.replace(' ', '_')
    if key:
        st.header("Images of " + key)