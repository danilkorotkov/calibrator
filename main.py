import sys

# import PyQt4 QtCore and QtGui modules
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from calibrator import Calibrator

if __name__ == '__main__':

    # create application
    app = QApplication( sys.argv )
    app.setApplicationName( 'calibrator' )

    # create widget
    w = Calibrator()
    w.setWindowTitle( 'calibrator' )
    w.show()

    # connection
    QObject.connect( app, SIGNAL( 'lastWindowClosed()' ), app, SLOT( 'quit()' ) )

    # execute application
    sys.exit( app.exec_() )
