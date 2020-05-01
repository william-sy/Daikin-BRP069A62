import npyscreen

#
#self.mySlider = self.add(npyscreen.TitleSlider,name="Temp Indoor", lowest=12, out_of=30, step=1, label=True, block_color="WARNING", value=20)

class FormObject( npyscreen.FormWithMenus, npyscreen.SplitForm ):
    def create( self ):
        self.tc = self.add( npyscreen.TitleText, name="Temp Indoor:", value=20, editable=False, hidden=False)
        #self.add(npyscreen.BoxTitle, max_width=20, max_height=4,rely=4, name=self.tc.name,scroll_exit=True, values=[self.tc.value])

        self.nextrely += -1
        self.nextrelx += 55
        self.tc = self.add( npyscreen.TitleText, name="Temp Outdoor:", value=10, editable=False, hidden=False)
        self.nextrelx += -55
        self.nextrely += 1
        self.tc = self.add( npyscreen.TitleText, name="Temp Target:", value=21, editable=False, hidden=False)
        self.nextrely += -1
        self.nextrelx += 55
        self.add( npyscreen.TitleText,name="Temp Water:",value=44,editable=False,hidden=False)
        self.nextrelx += -55
        self.nextrely += 2
        self.add( npyscreen.TitleText,name="Status:",value="ON",editable=False,hidden=False)



        self.menu = self.new_menu( name="Main Menu", shortcut='1' )
        self.submenu = self.menu.addNewSubmenu( "Schedules:", '1' )
        self.submenu.addItem( "Current schedule", self.about , '0' )
        self.menu.addItem( "About", self.about, "^A")
        self.menu.addItem( "Exit Application", self.exit, "^X")

    def exit( self ):
        self.parentApp.switchForm( None )

    def about( self ):
        about_message = "[DHPCC] - Daikin Heatpump Control Center \nGoal: To control your Daikin heatpump \nVersion: 0.1 \nAuthor: William \nBugs, help: github.com"
        npyscreen.notify_confirm( about_message, title="About", editw=1 )

    def afterEditing( self ):
        pass #self.parentApp.setNextForm( None )

    def on_ok( self ):
        npyscreen.notify_wait("Changed Temp", title="Super Hot", form_color='STANDOUT')
        self.tc.value = self.tc.value + 50

    def on_cancel( self ):
        exit = npyscreen.notify_ok_cancel("Are you sure you want to cancell?", title="Exit?", editw=1)
        if ( exit ):
            self.parentApp.setNextForm( None )
        else:
            pass




class App( npyscreen.NPSAppManaged ):
    def onStart( self ):
        self.addForm('MAIN',
                        FormObject,
                        name = 'DHPCC',
                        lines=24,
                        columns=80,
                        draw_line_at = 21
                    )

if ( __name__ == "__main__" ):
    app = App().run()
