#ifndef UI_QT_IMG_H
#define UI_QT_IMG_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QToolBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_Qt_imgClass
{
public:
　　QWidget *centralWidget;
　　QWidget *widget1;
　　QMenuBar *menuBar;
　　QToolBar *mainToolBar;
　　QStatusBar *statusBar;

　　void setupUi(QMainWindow *Qt_imgClass)
　　{
　　　　if (Qt_imgClass->objectName().isEmpty())
　　　　　　Qt_imgClass->setObjectName(QString::fromUtf8("Qt_imgClass"));
　　　　    Qt_imgClass->resize(895, 628);
    　　　　centralWidget = new QWidget(Qt_imgClass);
    　　　　centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
    　　　　widget1 = new QWidget(centralWidget);
    　　　　widget1->setObjectName(QString::fromUtf8("widget1"));
    　　　　widget1->setGeometry(QRect(360, 40, 471, 371));
    　　　　Qt_imgClass->setCentralWidget(centralWidget);
    　　　　menuBar = new QMenuBar(Qt_imgClass);
    　　　　menuBar->setObjectName(QString::fromUtf8("menuBar"));
    　　　　menuBar->setGeometry(QRect(0, 0, 895, 26));
    　　　　Qt_imgClass->setMenuBar(menuBar);
    　　　　mainToolBar = new QToolBar(Qt_imgClass);
    　　　　mainToolBar->setObjectName(QString::fromUtf8("mainToolBar"));
    　　　　Qt_imgClass->addToolBar(Qt::TopToolBarArea, mainToolBar);
    　　　　statusBar = new QStatusBar(Qt_imgClass);
    　　　　statusBar->setObjectName(QString::fromUtf8("statusBar"));
    　　　　Qt_imgClass->setStatusBar(statusBar);

　　　　retranslateUi(Qt_imgClass);

　　　　QMetaObject::connectSlotsByName(Qt_imgClass);
　　} // setupUi

　　void retranslateUi(QMainWindow *Qt_imgClass)
　　{
　　　　Qt_imgClass->setWindowTitle(QApplication::translate("Qt_imgClass", "Qt_img", nullptr));
　　} // retranslateUi

};

namespace Ui {
　　class Qt_imgClass: public Ui_Qt_imgClass {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_QT_IMG_H