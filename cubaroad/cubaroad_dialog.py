# -*- coding: utf-8 -*-
"""
/***************************************************************************
 cubaroadDialog
                                 A QGIS plugin
 This is an adaptation of the CubaRoad app for in qgis uses
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2024-03-27
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Cosylval
        email                : yoann.zenner@viacesi.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
from qgis.PyQt import uic, QtWidgets
from .CubaRoad_1_function import apply_cubaroad
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.PyQt.QtCore import QCoreApplication

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'cubaroad_dialog_base.ui'))


class cubaroadDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self,iface=None, parent=None):
        """Constructor."""
        super(cubaroadDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.setWindowTitle("SylvaRoad")
        #self.setWindowIcon(QIcon(':/plugins/sylvaccess_plugin/icon.png'))
        self.iface = iface
        global Cubaroad_UI
        Cubaroad_UI = self

        ##################################################################
        #.______     ______    __    __  .__________.  ______   .__   __.# 
        #|   _  \   /  __  \  |  |  |  | |          | /  __  \  |  \ |  |# 
        #|  |_)  | |  |  |  | |  |  |  | `---|  |---`|  |  |  | |   \|  |# 
        #|   _  <  |  |  |  | |  |  |  |     |  |    |  |  |  | |  . `  |# 
        #|  |_)  | |  `--'  | |  `--'  |     |  |    |  `--'  | |  |\   |# 
        #|______/   \______/   \______/      |__|     \______/  |__| \__|# 
        ################################################################## 
        
        for i in range(1, 5):
            button = getattr(self, f"pushButton_{i}")
            button.clicked.connect(lambda _, num=i: self.open_folder(num))

    def open_folder(self, button_number):
        # Définit les filtres génériques pour Shapefiles et fichiers raster
        shapefile_filter = "Shapefiles (*.shp );;Geopackage(*.gpkg);;All files (*)"
        raster_filter = "Raster files (*.tif *.asc *.txt);;All files (*)"

        # Définit les options de la boîte de dialogue
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog

        # Affiche le dialogue de sélection de fichier avec les filtres appropriés
        if button_number == 3:
            selected_file, _ = QFileDialog.getOpenFileName(None, QCoreApplication.translate("MainWindow","Select a file"), filter=shapefile_filter, options=options)
        elif button_number == 2:
            selected_file, _ = QFileDialog.getOpenFileName(None, QCoreApplication.translate("MainWindow","Select a file"), filter=raster_filter, options=options)
        elif button_number in [1, 4]: 
            selected_file = QFileDialog.getExistingDirectory(None, QCoreApplication.translate("MainWindow","Select a folder"), options=options)

        if selected_file:
            text_edit = getattr(self, f"lineEdit_{button_number}")
            text_edit.setText(selected_file)



    #####################################################################################################################
    #  _______  _______ .___________.   ____    ____  ___      .______    __       ___      .______    __       _______ #
    # /  _____||   ____||           |   \   \  /   / /   \     |   _  \  |  |     /   \     |   _  \  |  |     |   ____|#
    #|  |  __  |  |__   `---|  |----`    \   \/   / /  ^  \    |  |_)  | |  |    /  ^  \    |  |_)  | |  |     |  |__   #
    #|  | |_ | |   __|      |  |          \      / /  /_\  \   |      /  |  |   /  /_\  \   |   _  <  |  |     |   __|  #
    #|  |__| | |  |____     |  |           \    / /  _____  \  |  |\  \-.|  |  /  _____  \  |  |_)  | |  `----.|  |____ #
    # \______| |_______|    |__|            \__/ /__/     \__\ | _| `.__||__| /__/     \__\ |______/  |_______||_______|#
    #####################################################################################################################


    def get_var(self):
        Wspace = self.lineEdit_1.text()
        Wspace += '/'
        Dtm_file = self.lineEdit_2.text()
        Dtm_file += '/'
        Road_file = self.lineEdit_3.text()
        Road_file += '/'
        Res_dir = self.lineEdit_4.text()
        from_Sylvaroad = self.checkBox_1.isChecked()    # True if Road_file from SylvaRoad / False if Road_file is not from SylvaRoad
        step = self.spinBox_1.value()                   # [m] Step of analysis
        max_exca_slope = self.spinBox_2.value()         # [%] Cross slope beyond which 100% of material is excavated
        min_exca_slope = self.spinBox_3.value()         # [%] Inferior threshold of cross slope to start skidding the road axis
        z_tolerance = self.spinBox_4.value()            # [cm] tolerance to consider an intercetion with terrain
        xy_tolerance = self.spinBox_5.value()           # [m] buffer around theoretical axis of the road 
        if xy_tolerance == -1: xy_tolerance = None      # Put -1 to have xy_tolerance = 0.5*road_width
        save_fig = self.checkBox_2.isChecked()          # Save (True) or not (False) the ground profile of each calculation point  
        save_shp = self.checkBox_3.isChecked()          # Save (True) or not (False) the point of analyse and transects
        Radius = self.spinBox_6.value()                 # [m] Radius of lace turns
        angle_hairpin = self.spinBox_7.value()          # [°] Min angle to be considered as lace turn

        return Wspace,Dtm_file,Road_file,Res_dir,from_Sylvaroad,step,max_exca_slope,min_exca_slope,z_tolerance,xy_tolerance,save_fig,save_shp,Radius,angle_hairpin


    ################################################################################
    ### Script execution
    ################################################################################

    def run(self):
        Wspace,Dtm_file,Road_file,Res_dir,from_Sylvaroad,step,max_exca_slope,min_exca_slope,z_tolerance,xy_tolerance,save_fig,save_shp,Radius,angle_hairpin =Cubaroad_UI.get_var()
        
        if 'Wspace' not in locals() or 'Wspace' not in globals() :
            Wspace = Res_dir


        #Run road designer 
        apply_cubaroad(Dtm_file,Road_file,Res_dir,step,max_exca_slope,min_exca_slope,z_tolerance,  
                       xy_tolerance,save_fig,save_shp,Wspace,from_Sylvaroad,Radius,angle_hairpin)

