#
#
###Updated By Emircan Demirci 2.12.2020
#
#
import PyQt5
from PyQt5 import QtWidgets , QtCore , QtGui
from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
from PyQt5.QtGui import*
import sys

def mask_image(imgdata, imgtype='jpg', size=256):
    """Return a ``QPixmap`` from *imgdata* masked with a smooth circle.

    *imgdata* are the raw image bytes, *imgtype* denotes the image type.

    The returned image will have a size of *size* × *size* pixels.

    """
    # Load image and convert to 32-bit ARGB (adds an alpha channel):
    image = QImage.fromData(imgdata, imgtype)
    image.convertToFormat(QImage.Format_ARGB32)

    # Crop image to a square:
    imgsize = min(image.width(), image.height())
    rect = QRect(
        (image.width() - imgsize) / 2,
        (image.height() - imgsize) / 2,
        imgsize,
        imgsize,
    )
    image = image.copy(rect)

    # Create the output image with the same dimensions and an alpha channel
    # and make it completely transparent:
    out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
    out_img.fill(Qt.transparent)

    # Create a texture brush and paint a circle with the original image onto
    # the output image:
    brush = QBrush(image)        # Create texture brush
    painter = QPainter(out_img)  # Paint the output image
    painter.setBrush(brush)      # Use the image texture brush
    painter.setPen(Qt.NoPen)     # Don't draw an outline
    painter.setRenderHint(QPainter.Antialiasing, True)  # Use AA
    painter.drawEllipse(0, 0, imgsize, imgsize)  # Actually draw the circle
    painter.end()                # We are done (segfault if you forget this)

    # Convert the image to a pixmap and rescale it.  Take pixel ratio into
    # account to get a sharp image on retina displays:
    pr = QWindow().devicePixelRatio()
    pm = QPixmap.fromImage(out_img)
    pm.setDevicePixelRatio(pr)
    size *= pr
    pm = pm.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    return pm

class HomeScreen(QWidget):
    binds = {"add_friend": None, "search_friend": None} # binding names can change.
    def __init__(self):
        super(HomeScreen , self).__init__()
        self.mainLayout = QVBoxLayout() #apps main layout
        self.mainLayout.addWidget(TitleBar(self))

        self.initLayout()
        
        self.mainLayout.addLayout(self.objectsLayout)

        #main menu main objects
        self.setStyleSheet("background-color:#262626;")
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.sizegrip = QtWidgets.QSizeGrip(self)
        self.setWindowFlags(Qt.FramelessWindowHint |  QtCore.Qt.WindowStaysOnTopHint)
        self.setMinimumSize(1080,700)
        self.setLayout(self.mainLayout)
        
        self.pp_path = "Buttons/unnamed.gif"

        self.initStackedWidgets()
        self.initMainLeftMenu()
        self.initHomePage()
        self.initFriendsPage()
        self.initProfilePage()
        self.initSettingsPage()
        self.initEditProfile()
        self.addWidgetsToLayout()

        self.show()
    
    @classmethod
    def bind(cls,name):
        assert (name in cls.binds)

        def getFunc(func):
            cls.binds[name] = func
        return getFunc 
    
    #initialize Layouts
    def initLayout(self):
        #all objects layout
        self.objectsLayout = QHBoxLayout()
        self.objectsLayout.setContentsMargins(0,0,0,0)
        self.objectsLayout.addSpacing(0)
        #all menusLayout
        self.menusLayout = QVBoxLayout()
        self.menusLayout.setContentsMargins(0,0,0,0)
        self.menusLayout.addSpacing(-6)
        #all mainobjects layout
        self.mainobjectsLayout = QVBoxLayout()
        self.mainobjectsLayout.setContentsMargins(0,0,0,0)
        self.mainobjectsLayout.addSpacing(1)
        #main page all layouts layout
        self.allmain_page_layouts = QVBoxLayout()
        self.allmain_page_layouts.setContentsMargins(0,0,0,0)
        #main page layout
        self.main_page_layout = QHBoxLayout()
        self.main_page_layout.setContentsMargins(0,0,0,0)
        #main page vbox layout
        self.main_page_vbox = QVBoxLayout()
        self.main_page_layout.setContentsMargins(0,0,0,0)
        self.objectsLayout.addLayout(self.menusLayout)
        self.objectsLayout.addLayout(self.mainobjectsLayout)
        #all friends page layout
        self.friends_page_objects_layout = QVBoxLayout()
        self.friends_page_objects_layout.setContentsMargins(0,0,5,0)
        self.friends_page_objects_layout.addSpacing(0)
        #main friends layout
        self.myFriendsLayout = QVBoxLayout()
        self.myFriendsLayout.setContentsMargins(0,0,0,0)
        #friends menu layout 
        self.friendsmenu_layout = QHBoxLayout()
        self.friendsmenu_layout.setContentsMargins(0,0,0,0)
        #pending request layout
        self.pending_rqst_Layout = QVBoxLayout()
        self.pending_rqst_Layout.setContentsMargins(0,0,0,0)
        #search layout
        self.searchLayout = QVBoxLayout()
        self.searchLayout.setContentsMargins(0,0,0,0)
        #profile page layout
        self.profile_page_layout = QVBoxLayout()
        self.profile_page_layout.setContentsMargins(0,0,0,0)
        #settings layout
        self.settings_page_layout = QVBoxLayout()
        self.settings_page_layout.setContentsMargins(0,0,0,0)
        #settings profile scroll layout
        self.profile_settings_scroll = QScrollArea()
        self.profile_settings_scroll.setWidgetResizable(True)
        self.profile_settings_scroll.setStyleSheet("""QScrollArea
        {
            border:none;
            margin-right:5px;
        }""")
        self.profile_settings_scroll.verticalScrollBar().setStyleSheet(""" QScrollBar:vertical{
        border: 2px solid grey;
        background: #262626;
        border-radius: 4px;
        }
        QScrollBar QWidget{
            background-color:transparent;
        }
        QScrollBar::handle:vertical
        {
            background-color:#141414;         /* #605F5F; */
            min-height: 5px;
            border-radius: 4px;
            width:50px;
        }
        
        QScrollBar::add-line:vertical
        {
            margin: 0px 3px 0px 3px;
            width: 10px;
            height: 10px;
            subcontrol-position: right;
            subcontrol-origin: margin;
            background:none;
            color:none;
        }

        QScrollBar::sub-line:vertical
        {
            margin: 0px 3px 0px 3px;
            height: 10px;
            width: 10px;
            subcontrol-position: left;
            subcontrol-origin: margin;
            background:none;
            color:none;}""")
        #profile settings layout
        self.profile_settings_layout = QVBoxLayout()
        self.profile_settings_layout.setContentsMargins(0,0,0,0)
        #settings menu layout
        self.settings_menu_layout = QHBoxLayout()
        self.settings_menu_layout.setContentsMargins(0,0,0,0)
        #edit profile layout
        self.edit_profile_layout = QVBoxLayout()
        self.edit_profile_layout.setContentsMargins(0,0,0,0)
        #edit profile scroll bar
        self.edit_profile_scroll = QScrollArea()
        self.edit_profile_scroll.setWidgetResizable(True)
        self.edit_profile_scroll.setStyleSheet("""QScrollArea
        {
            border:none;
            margin-right:5px;
        }""")
        self.edit_profile_scroll.verticalScrollBar().setStyleSheet(""" QScrollBar:vertical{
        border: 2px solid grey;
        background: #262626;
        border-radius: 4px;
        }
        QScrollBar QWidget{
            background-color:transparent;
        }
        QScrollBar::handle:vertical
        {
            background-color:#141414;         /* #605F5F; */
            min-height: 5px;
            border-radius: 4px;
            width:50px;
        }
        
        QScrollBar::add-line:vertical
        {
            margin: 0px 3px 0px 3px;
            width: 10px;
            height: 10px;
            subcontrol-position: right;
            subcontrol-origin: margin;
            background:none;
            color:none;
        }

        QScrollBar::sub-line:vertical
        {
            margin: 0px 3px 0px 3px;
            height: 10px;
            width: 10px;
            subcontrol-position: left;
            subcontrol-origin: margin;
            background:none;
            color:none;}""")
        #edit profile buttons layout
        self.edit_buttons_layout = QHBoxLayout()
        self.edit_buttons_layout.setContentsMargins(0,0,0,0)
    #initialize HomeScreen
    def initHomePage(self):
        ######################################
        ##Main objects
        ######################################
        self.welcome_label = QLabel("<h1>Welcome to the</h1>" , self.mainscreen_objects_widget)
        self.welcome_label.setAlignment(Qt.AlignRight)
        self.welcome_label.setFont(QFont('Arial' , 15))
        self.main_page_layout.addWidget(self.welcome_label)
        self.welcome_label.setStyleSheet("""QLabel{
            color:#F2F2EB;
        }""")

        self.codeDuel_label = QLabel("<h1><font color='red'>Code</font>Duel<h1>" , self.mainscreen_objects_widget)
        self.codeDuel_label.setStyleSheet("""QLabel{
            color:orange; 
            margin-left:10px;
        }""")
        self.codeDuel_label.setAlignment(Qt.AlignLeft)
        self.codeDuel_label.setFont(QFont('Arial' , 15))
        self.main_page_layout.addWidget(self.codeDuel_label)

        self.what_is_app_title = QLabel("<h2>What is <font color = 'red'>Code</font><font color = 'orange'>Duel</font>?</h2>" , self.mainscreen_objects_widget)
        self.what_is_app_title.setStyleSheet("""QLabel{
            color:#F2F2EB;
            margin-left:10px;
        }""")
        self.what_is_app_title.setFixedHeight(60)
        self.what_is_app_title.setFont(QFont('Arial' , 15))
        self.what_is_app_title.setAlignment(Qt.AlignLeft)
        self.main_page_vbox.addWidget(self.what_is_app_title)
        self.about_codeDuel = QLabel("<strong>With CodeDuel, you can fight codes with your friends.The first person <br>who finds the problem will win the duel.<br>If you are new, you can learn the game from our site!<br><a href='http://code-duel.com/'><font color = red>Code</font><font color = orange>Duel</font></a></strong>" , self.mainscreen_objects_widget)
        self.about_codeDuel.setOpenExternalLinks(True)
        self.about_codeDuel.setFont(QFont('Arial' ,20))
        self.about_codeDuel.setStyleSheet("""QLabel{
            color:#F2F2EB;
            margin-right:20px;
        }""")
        self.about_codeDuel.setAlignment(Qt.AlignHCenter)
        self.main_page_vbox.addWidget(self.about_codeDuel)
    
    #initialize all stackedwidgets
    def initStackedWidgets(self):
        #stacked widgets

        #######################################
        ##Left Menus
        #######################################
        self.all_left_menus_stacked_wiget = QStackedWidget()
        self.all_left_menus_stacked_wiget.setFixedWidth(100)
        self.menusLayout.addWidget(self.all_left_menus_stacked_wiget)

        self.main_left_menu_widget = QWidget()
        self.all_left_menus_stacked_wiget.addWidget(self.main_left_menu_widget)

        self.profile_page_left_menu_widget = QWidget()
        self.all_left_menus_stacked_wiget.addWidget(self.profile_page_left_menu_widget)

        #######################################
        ##Main Objects 
        #######################################
        self.main_objects_stacked_widget = QStackedWidget()
        self.mainobjectsLayout.addWidget(self.main_objects_stacked_widget)

        self.mainscreen_objects_widget = QWidget()
        self.main_objects_stacked_widget.addWidget(self.mainscreen_objects_widget)

        self.mainscreen_objects_widget.setLayout(self.allmain_page_layouts)
        self.allmain_page_layouts.addLayout(self.main_page_layout)
        self.allmain_page_layouts.addLayout(self.main_page_vbox , Qt.AlignRight)

        self.friends_screen_widget = QWidget()
        self.main_objects_stacked_widget.addWidget(self.friends_screen_widget)
        self.friends_screen_widget.setLayout(self.friends_page_objects_layout)
        self.friends_page_objects_layout.addLayout(self.friendsmenu_layout , Qt.AlignTop)

        self.profile_page_widget = QWidget()
        self.main_objects_stacked_widget.addWidget(self.profile_page_widget)
        self.profile_page_widget.setLayout(self.profile_page_layout)

        self.settings_page_widget = QWidget()
        self.main_objects_stacked_widget.addWidget(self.settings_page_widget)
        self.settings_page_widget.setLayout(self.settings_page_layout)
        
        self.settings_page_layout.addLayout(self.settings_menu_layout , Qt.AlignTop)
        ################################################################################
        ##Friends Menu Widgets
        #################################################################################
        self.friends_Stacked_widget = QStackedWidget()
        self.friends_page_objects_layout.addWidget(self.friends_Stacked_widget)

        self.myFriendsWidget = QWidget()
        self.friends_Stacked_widget.addWidget(self.myFriendsWidget)
        self.myFriendsWidget.setLayout(self.myFriendsLayout)

        self.pending_rqst_widget = QWidget()
        self.friends_Stacked_widget.addWidget(self.pending_rqst_widget)
        self.pending_rqst_widget.setLayout(self.pending_rqst_Layout)

        self.search_lineedit_widget = QWidget()
        self.friends_Stacked_widget.addWidget(self.search_lineedit_widget)
        self.search_lineedit_widget.setLayout(self.searchLayout)
        #########################################################################
        ##settings widgets
        #########################################################################
        self.settings_stacked_widget = QStackedWidget()
        self.settings_page_layout.addWidget(self.settings_stacked_widget)

        self.profile_settings_page = QWidget()
        self.profile_settings_page.setLayout(self.profile_settings_layout)
        self.profile_settings_scroll.setWidget(self.profile_settings_page)

        self.settings_stacked_widget.addWidget(self.profile_settings_scroll)

        self.edit_profile_page = QWidget()
        self.edit_profile_page.setLayout(self.edit_profile_layout)
        self.edit_profile_scroll.setWidget(self.edit_profile_page)
        self.settings_stacked_widget.addWidget(self.edit_profile_scroll)

        

    def addWidgetsToLayout(self):
        ##########################################
        ##Layouts
        #########################################

        #friends top menu
        self.friendsmenu_layout.addWidget(self.my_friends_btn)
        self.friendsmenu_layout.addWidget(self.pending_rqst_btn)
        self.friendsmenu_layout.addWidget(self.ghostLabel2)
        self.friendsmenu_layout.addWidget(self.search_lineedit)
        self.friendsmenu_layout.addWidget(self.search_btn)

        #my friends page
        self.myFriendsLayout.addWidget(self.myfriends_page_label)

        #pending requests page
        self.pending_rqst_Layout.addWidget(self.pendingrqst_page_label)

        #search page
        self.searchLayout.addWidget(self.search_page_label)

        #profile page
        self.profile_page_layout.addWidget(self.profile_page_photo)
        self.profile_page_layout.addWidget(self.profile_username)
        self.profile_page_layout.addWidget(self.previous_matches)

        #settings page        
        self.settings_menu_layout.addWidget(self.profile_settings_btn , Qt.AlignCenter)
        self.settings_menu_layout.addWidget(self.settings_ghost_label)

        #profile settings page
        self.profile_settings_layout.addWidget(self.profile_settings_label)
        self.profile_settings_layout.addWidget(self.profile_settings_photo)
        self.profile_settings_layout.addWidget(self.settings_username)
        self.profile_settings_layout.addWidget(self.user_email)
        self.profile_settings_layout.addWidget(self.edit_profile_btn , alignment = Qt.AlignTop)
        self.profile_settings_layout.addWidget(self.change_password_label)
        self.profile_settings_layout.addWidget(self.change_password)
        
        #edit profile button clicked
        self.edit_profile_layout.addWidget(self.edit_profile_pp)
        self.edit_profile_layout.addWidget(self.edit_username)
        self.edit_profile_layout.addWidget(self.edit_email)
        self.edit_profile_layout.addLayout(self.edit_buttons_layout) 
        self.edit_buttons_layout.addWidget(self.save_changes_btn)
        self.edit_buttons_layout.addWidget(self.cancel_btn)

        #sizegrip
        self.mainLayout.addWidget(self.sizegrip,0,Qt.AlignBottom|Qt.AlignRight)
    
    #initialize Friends Page
    def initFriendsPage(self):
        ###########################################################
        ##Friends Screen
        ###########################################################

        #search page
        self.search_page_label = QLabel("check the name or the 4 digit number!")
        self.search_page_label.setAlignment(Qt.AlignCenter)
        self.search_page_label.setFont(QFont('Arial' , 25))
        self.search_page_label.setStyleSheet("color:#F2F2EB")
        
        #pending requests page
        self.pendingrqst_page_label = QLabel("You dont have any requests.")
        self.pendingrqst_page_label.setAlignment(Qt.AlignCenter)
        self.pendingrqst_page_label.setFont(QFont('Arial' , 25))
        self.pendingrqst_page_label.setStyleSheet("color:#F2F2EB")
        #my friends page
        self.myfriends_page_label = QLabel("I hope you have friends :(")
        self.myfriends_page_label.setAlignment(Qt.AlignCenter)
        self.myfriends_page_label.setFont(QFont('Arial' , 25))
        self.myfriends_page_label.setStyleSheet("color:#F2F2EB")

        #friends menu
        self.my_friends_btn = QPushButton("My Friends")
        self.my_friends_btn.setFixedSize(90,30)
        self.my_friends_btn.setStyleSheet("""QPushButton{
            background-color:#8C8C8C;
            border:none;
            color:#141414;
        }
        QPushButton:hover{
            border-bottom: 4px solid #5C5C5C;
        }""")
        self.my_friends_btn.clicked.connect(self.my_friends_btn_clicked)

        self.pending_rqst_btn = QPushButton("Pending Requests")
        self.pending_rqst_btn.setFixedSize(90,30)
        self.pending_rqst_btn.setStyleSheet("""QPushButton{
            background-color:#8C8C8C;
            border:none;
            color:#141414;
        }
        QPushButton:hover{
            border-bottom: 4px solid #5C5C5C;
        }""")
        self.pending_rqst_btn.clicked.connect(self.pending_rqst_btn_cliked)

        self.search_lineedit = QLineEdit()
        self.search_lineedit.setPlaceholderText("Search your friends, you must write name#0000")
        self.search_lineedit.setFixedSize(400,30)
        self.search_lineedit.setFont(QFont('Arial' , 10))
        self.search_lineedit.setStyleSheet("""QLineEdit{
            border: 3px solid #5C5C5C;
            color:#F2F2EB;
            background-color:#5c5c5c
        }""")
        
        self.search_btn = QPushButton("Search")
        self.search_btn.setFixedSize(90,30)
        self.search_btn.setStyleSheet("""QPushButton{
            background-color:#8C8C8C;
            border:none;
            color:#141414;
        }
        QPushButton:hover{
            border-bottom: 4px solid #5C7B5C;
        }""")
        self.search_btn.clicked.connect(self.search_btn_clicked)

        #ghost label (inactive label)
        self.ghostLabel2 = QLabel()
        self.ghostLabel2.setStyleSheet("""background-color:#8C8C8C;""")
        self.ghostLabel2.setAlignment(Qt.AlignCenter)
        self.ghostLabel2.setFixedHeight(30)
    
    #initialize Profile Page
    def initProfilePage(self):
        ##################################
        ##profile page
        ##################################
        self.match_number = 0
        self.previous_matches = QLabel("Previous Matches:" + str(self.match_number))
        self.previous_matches.setStyleSheet("""QLabel{
            color:#F2F2EB;
            margin-top:10px;
            font-size:32px;
        }""")
        self.previous_matches.setAlignment(Qt.AlignHCenter)

        self.profile_username = QLabel("Username")
        self.profile_username.setAlignment(Qt.AlignHCenter)
        self.profile_username.setStyleSheet("""QLabel{
            color:#F2F2EB;
            margin-top:10px;
            font-size:32px;
        }""")
        
        self.profile_photo_data = open(self.pp_path, 'rb').read()
        self.profile_photo_pixmap = mask_image(self.profile_photo_data)

        self.profile_page_photo = QLabel()
        self.profile_page_photo.setAlignment(Qt.AlignCenter) 
        self.profile_page_photo.setPixmap(self.profile_photo_pixmap)
        self.profile_page_photo.setFixedHeight(300)
        self.profile_page_photo.setStyleSheet("""QLabel{
            margin:300px;
            border:none;
        }""")
        
        #profile page left menu object
        self.go_to_mainmenu = QPushButton('' , self.profile_page_left_menu_widget)
        self.go_to_mainmenu.setIcon(QIcon("Buttons/settingsGoBackbtn.png"))
        self.go_to_mainmenu.setGeometry(10,10,35,35)
        self.go_to_mainmenu.setStyleSheet("""QPushButton{
            background-color:#595959;
            border:none;
        }
        QPushButton:hover{
            border-bottom:4px solid rgb(0,191,255);
        }""")
        self.go_to_mainmenu.clicked.connect(self.go_to_mainmenu_clicked)
    
    
    
    #initialize Main Page Left Menu
    def initMainLeftMenu(self):
        ######################################
        ##left menu
        ######################################
        self.ghostLabel = QLabel(self.main_left_menu_widget)
        self.ghostLabel.resize(100,16770)
        self.ghostLabel.setStyleSheet("background-color:#141414;")

        self.profile_photo = QPushButton(self.main_left_menu_widget)
        self.profile_photo.setIcon(QIcon(self.pp_path))
        self.profile_photo.setIconSize(QSize(64,64))
        self.profile_photo.setFixedSize(50,50)
        self.profile_photo.move(25,0)
        self.region = QRegion(self.profile_photo.rect() , QRegion.Ellipse)
        self.profile_photo.setMask(self.region)
        self.profile_photo.clicked.connect(self.profile_photo_clicked)

        #main left menu home button       
        self.home_button = QPushButton('' , self.main_left_menu_widget)
        self.home_button.setIcon(QIcon("Buttons/homeButton2.png"))
        self.home_button.setGeometry(-2,80,105,50)
        self.home_button.setStyleSheet("""QPushButton{
            background-color:#595959;
            border:none;
        }
        QPushButton:hover{
            border-bottom: 4px solid qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(0,191,255),stop:1 rgba(0, 0, 0, 0));
        }""")
        self.home_button.clicked.connect(self.home_button_clicked)
        self.home_button.setIconSize(QSize(20,20))


        #main left menu settings button
        self.settings_btn = QPushButton('' , self.main_left_menu_widget)
        self.settings_btn.setIcon(QIcon("Buttons/yourFriends.png"))
        self.settings_btn.setGeometry(-2,130,105,50)
        self.settings_btn.setStyleSheet("""QPushButton{
            background-color:#595959;
            border:none;
            margin-top:2px;
        }
        QPushButton:hover{
            border-bottom: 4px solid qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(0,191,255),stop:1 rgba(0, 0, 0, 0));
        }""")
        self.settings_btn.clicked.connect(self.friends_btn_clicked)
        self.settings_btn.setIconSize(QSize(20,20))

        self.settings_btn = QPushButton('' , self.main_left_menu_widget)
        self.settings_btn.setIcon(QIcon('Buttons/settingsBtn.png'))
        self.settings_btn.setGeometry(-2,180,105,50)
        self.settings_btn.setStyleSheet("""QPushButton{
            background-color:#595959;
            border:none;
            margin-top:2px;
        }
        QPushButton:hover{
            border-bottom: 4px solid qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(0,191,255),stop:1 rgba(0, 0, 0, 0));
        }""")
        self.settings_btn.clicked.connect(self.settings_btn_clicked)
        self.settings_btn.setIconSize(QSize(20,20))

    def initSettingsPage(self):     
        #profile settings title
        self.profile_settings_label = QLabel("<h1><strong><font style='color:#bfbfbf'>Profile</font></strong></h1>")

        #ghostLabel
        self.settings_ghost_label = QLabel()
        self.settings_ghost_label.setStyleSheet("""QLabel{
            background-color:#8C8C8C;
            margin-right:5px;
        }""")
        self.settings_ghost_label.setAlignment(Qt.AlignCenter)
        self.settings_ghost_label.setFixedHeight(30)

        #profile settings button
        self.profile_settings_btn = QPushButton("Profile")
        self.profile_settings_btn.setStyleSheet("""QPushButton{
            background-color:#8C8C8C;
            border:none;
        }
        QPushButton:hover{
            border-bottom: 4px solid #5c5c5c;
        }""")
        self.profile_settings_btn.setFixedHeight(30)
        self.profile_settings_btn.setFixedWidth(90)
        self.profile_settings_btn.clicked.connect(self.profile_settings_btn_clicked)

        self.user_email = QLabel("Email")
        self.user_email.setAlignment(Qt.AlignHCenter)
        self.user_email.setStyleSheet("""QLabel{
            color:#F2F2EB;
            font-size:32px;
        }""")

        #username
        self.settings_username = QLabel("Username")
        self.settings_username.setAlignment(Qt.AlignHCenter)
        self.settings_username.setStyleSheet("""QLabel{
            color:#F2F2EB;
            margin-top:10px;
            font-size:32px;
        }""")

        #profile photo
        self.profile_settings_photo = QLabel()
        self.profile_settings_photo.setAlignment(Qt.AlignCenter) 
        self.profile_settings_photo.setPixmap(self.profile_photo_pixmap)
        self.profile_settings_photo.setFixedHeight(300)
        self.profile_settings_photo.setStyleSheet("""QLabel{
            border:none;
        }""")

        #edit profile button 
        self.edit_profile_btn = QPushButton("Edit Profile")
        self.edit_profile_btn.setStyleSheet("""QPushButton{
            background-color:#8C8C8C;
            border:none;
            margin-left:300px;
            margin-right:300px;
        }
        QPushButton:hover{
            border-bottom: 4px solid rgb(0,191,255);
        }""")
        self.edit_profile_btn.setFixedHeight(30)
        self.edit_profile_btn.clicked.connect(self.edit_profile_btn_clicked)

        #change password title
        self.change_password_label = QLabel("<h1><strong><font style='color:#bfbfbf'>Password</font></strong></h1>")
        self.change_password_label.setStyleSheet("margin-top:50px;")

        #change password
        self.change_password= QPushButton("Change Password")
        self.change_password.setStyleSheet("""QPushButton{
            background-color:#8C8C8C;
            border:none;
            margin-right:500px;
            margin-left:50px
        }
        QPushButton:hover{
            border-bottom: 4px solid rgb(0,191,255);
        }""")
        self.change_password.setFixedHeight(30)
        self.change_password.clicked.connect(self.change_password_btn_clicked)

    def initEditProfile(self):
        self.edit_profile_pp = QLabel()
        self.edit_profile_pp.setAlignment(Qt.AlignCenter) 
        self.edit_profile_pp.setPixmap(self.profile_photo_pixmap)
        self.edit_profile_pp.setFixedHeight(300)
        self.edit_profile_pp.setStyleSheet("""QLabel{
            border:none;
        }""")

        self.edit_username = QPlainTextEdit()
        self.edit_username.setStyleSheet("""QPlainTextEdit{
            border: 3px solid dimgray;
            border-style:outset;border-width:2px;
            border-radius:10px;
            color:silver;
            margin-left:300px;
            margin-right:300px;
            font-size:20px;
        }""")
        self.edit_username.setPlainText("Username")
        self.edit_username.setFixedHeight(40)

        self.edit_email = QPlainTextEdit()
        self.edit_email.setStyleSheet("""QPlainTextEdit{
            border: 3px solid dimgray;
            border-style:outset;
            border-width:2px;
            border-radius:10px;
            color:silver;
            margin-left:300px;
            margin-right:300px;
            font-size:20px;
        }""")
        self.edit_email.setPlainText("Email")
        self.edit_email.setFixedHeight(40)

        self.settings_stacked_widget.setCurrentIndex(1)

        self.save_changes_btn = QPushButton("Save Changes")
        self.save_changes_btn.setFixedHeight(35)
        self.save_changes_btn.setStyleSheet("""QPushButton{
            background-color:#8C8C8C;
            border:none;
        }
        QPushButton:hover{
            border-bottom: 4px solid rgb(0,191,255);
        }""")

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFixedHeight(35)
        self.cancel_btn.setStyleSheet("""QPushButton{
            background-color:#8C8C8C;
            border:none;
        }
        QPushButton:hover{
            border-bottom: 4px solid rgb(0,191,255);
        }""")
        self.cancel_btn.clicked.connect(self.cancel_btn_animation)

    #edit profile button clicked
    def edit_profile_btn_clicked(self , scroll):
        self.profile_settings_scroll.hide()
        
        QTimer.singleShot(400 , self.initEditProfile)

    #cancel btn clicked
    def cancel_btn_animation(self):
        self.edit_profile_scroll.hide()
        QTimer.singleShot(400 , self.edit_cancelbtn_clicked)

    def edit_cancelbtn_clicked(self):
        self.settings_stacked_widget.setCurrentIndex(0)
    #change password
    def change_password_btn_clicked(self):
        pass
    #home button clicked
    def home_button_clicked(self):
        self.main_objects_stacked_widget.setCurrentIndex(0)

    #friends button clicked
    def friends_btn_clicked(self):
        self.main_objects_stacked_widget.setCurrentIndex(1)

    #friends page topmenu my friends button clicked
    def my_friends_btn_clicked(self):
        self.friends_Stacked_widget.setCurrentIndex(0)

    #friends page topmenu pending requests button clicked
    def pending_rqst_btn_cliked(self):
        self.friends_Stacked_widget.setCurrentIndex(1)

    #friends page topmenu search button clicked
    def search_btn_clicked(self):
        self.friends_Stacked_widget.setCurrentIndex(2)

    #main left menu profile photo clicked
    def profile_photo_clicked(self):
        self.main_objects_stacked_widget.setCurrentIndex(2)
        self.all_left_menus_stacked_wiget.setCurrentIndex(1)

    #profile page go to main menu button (<-)
    def go_to_mainmenu_clicked(self):
        self.main_objects_stacked_widget.setCurrentIndex(0)
        self.all_left_menus_stacked_wiget.setCurrentIndex(0)
    
    #settings btn clicked
    def settings_btn_clicked(self):
        self.main_objects_stacked_widget.setCurrentIndex(3)
        self.settings_stacked_widget.setCurrentIndex(0)

    def profile_settings_btn_clicked(self):
        self.settings_stacked_widget.setCurrentIndex(0)


    
#titlebar
class TitleBar(QWidget):
    def __init__(self, parent):
        super(TitleBar, self).__init__()
        self.parent = parent
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.title = QLabel("CodeDuel")
        self.window_maximized = False

        btn_size = 35

        self.btn_close = QPushButton("✕")
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.setFixedSize(btn_size,btn_size)
        self.btn_close.setFlat(True)
        self.btn_close.move(750,0)
        self.btn_close.setStyleSheet("background-color: red;color:white;")

        self.btn_min = QPushButton("－")
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.setFixedSize(btn_size, btn_size)
        self.btn_min.move(600,0)
        self.btn_min.setFlat(True)
        self.btn_min.setStyleSheet("background-color: gray;color:white;")

        self.btn_max = QPushButton("☐")
        self.btn_max.clicked.connect(self.btn_max_clicked)
        self.btn_max.setFixedSize(btn_size, btn_size)
        self.btn_max.move(600,0)
        self.btn_max.setFlat(True)
        self.btn_max.setStyleSheet("background-color: gray;color:white;")

        self.title.setFixedHeight(35)
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_max)
        self.layout.addWidget(self.btn_close)


        self.title.setStyleSheet("""
            background-color: #141414;
            color:white;
        """)
        self.setLayout(self.layout)

        self.start = QPoint(0,0)
        self.pressing = False

    def resizeEvent(self, QResizeEvent):
        super(TitleBar, self).resizeEvent(QResizeEvent)
        self.title.setFixedWidth(self.parent.width())
    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                self.mapToGlobal(self.movement).y(),
                                self.parent.width(),
                                self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False




    def btn_close_clicked(self):
        self.parent.close()



    def btn_min_clicked(self):
        self.parent.showMinimized()

    def btn_max_clicked(self):
        self.parent.showMaximized()
        self.window_maximized = True
        if self.window_maximized == True:
            self.btn_max.disconnect()
            self.btn_max.setText("❐")
            self.btn_max.clicked.connect(self.restoreDownEvent)
    
    def restoreDownEvent(self):
        self.parent.showNormal()
        self.window_maximized = False

        if self.window_maximized == False:
            self.btn_max.disconnect()
            self.btn_max.setText("☐")
            self.btn_max.clicked.connect(self.btn_max_clicked)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = HomeScreen()
    ex.show()
    app.exec_()