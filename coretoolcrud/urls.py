
from django.urls import re_path as url
from django.urls import path
from .views import viewGrrXbarr, viewPrintGrrXbarr, viewCommentGrrXbarr, viewFinalGrrXbarr, storeGrrXbarr, storeAllGrrXbarr, storeCommentGrrXbarr, deleteGrrXbarr
from .views import viewCross, viewPrintCross, viewCommentCross, viewFinalCross, storeCross, storeCommentCross, storeAllCross, deleteCross
from .views import viewNested, viewPrintNested, viewCommentNested, viewFinalNested, storeNested, storeCommentNested, storeAllNested, deleteNested
from .views import viewLinearity, viewPrintLinearity, viewAverageLinearity, viewMasterLinearity, viewCommentLinearity, viewFinalLinearity, storeLinearity, storeMasterLinearity, storeAverageLinearity, storeCommentLinearity, storeAllLinearity, deleteLinearity
from .views import viewListSurvey, viewDetailSurvey, viewSurvey, viewManual, viewEditSurvey, viewEditManual, storeManual, storeSurvey, storeEditManual, storeEditSurvey, deleteSurvey
from .views import viewLogin, login, logout
app_name = "coretoolcrud"


urlpatterns = [

    path('',viewLogin),
    path('login',login,name='login'),
    path('logout',logout,name='logout'),

    path('viewListSurvey',viewListSurvey,name='viewListSurvey'),
    path('viewDetailSurvey/<int:pk>',viewDetailSurvey,name='viewDetailSurvey'),
    path('viewSurvey',viewSurvey,name='viewSurvey'),
    path('viewManual',viewManual,name='viewManual'),
    path('viewEditSurvey/<int:pk>',viewEditSurvey,name='viewEditSurvey'),
    path('viewEditManual/<int:pk>',viewEditManual,name='viewEditManual'),
    path('storeManual',storeManual,name='storeManual'),
    path('storeSurvey',storeSurvey,name='storeSurvey'),
    path('storeEditManual/<int:pk>',storeEditManual,name='storeEditManual'),
    path('storeEditSurvey/<int:pk>',storeEditSurvey,name='storeEditSurvey'),
    path('deleteSurvey/<int:pk>',deleteSurvey,name='deleteSurvey'),

    
    path('viewGrrXbarr/<int:pk>',viewGrrXbarr,name='viewGrrXbarr'),
    path('viewPrintGrrXbarr/<int:pk>',viewPrintGrrXbarr,name='viewPrintGrrXbarr'),
    path('viewFinalGrrXbarr/<int:pk>',viewFinalGrrXbarr,name='viewFinalGrrXbarr'),
    path('viewCommentGrrXbarr/<int:pk>',viewCommentGrrXbarr,name='viewCommentGrrXbarr'),
    path('storeGrrXbarr/<int:pk>',storeGrrXbarr,name='storeGrrXbarr'),
    path('storeAllGrrXbarr/<int:pk>',storeAllGrrXbarr,name='storeAllGrrXbarr'),
    path('storeCommentGrrXbarr/<int:pk>',storeCommentGrrXbarr,name='storeCommentGrrXbarr'),
    path('deleteGrrXbarr/<int:pk>',deleteGrrXbarr,name='deleteGrrXbarr'),

    path('viewCross/<int:pk>',viewCross,name='viewCross'),
    path('viewPrintCross/<int:pk>',viewPrintCross,name='viewPrintCross'),
    path('viewCommentCross/<int:pk>',viewCommentCross,name='viewCommentCross'),
    path('viewFinalCross/<int:pk>',viewFinalCross,name='viewFinalCross'),
    path('storeCross/<int:pk>',storeCross,name='storeCross'),
    path('storeAllCross/<int:pk>',storeAllCross,name='storeAllCross'),
    path('storeCommentCross/<int:pk>',storeCommentCross,name='storeCommentCross'),
    path('deleteCross/<int:pk>',deleteCross,name='deleteCross'),

    path('viewNested/<int:pk>',viewNested,name='viewNested'),
    path('viewPrintNested/<int:pk>',viewPrintNested,name='viewPrintNested'),
    path('viewCommentNested/<int:pk>',viewCommentNested,name='viewCommentNested'),
    path('viewFinalNested/<int:pk>',viewFinalNested,name='viewFinalNested'),
    path('storeNested/<int:pk>',storeNested,name='storeNested'),
    path('storeAllNested/<int:pk>',storeAllNested,name='storeAllNested'),
    path('storeCommentNested/<int:pk>',storeCommentNested,name='storeCommentNested'),
    path('deleteNested/<int:pk>',deleteNested,name='deleteNested'),

    path('viewLinearity/<int:pk>',viewLinearity,name='viewLinearity'),
    path('viewPrintLinearity/<int:pk>',viewPrintLinearity,name='viewPrintLinearity'),
    path('viewMasterLinearity/<int:pk>',viewMasterLinearity,name='viewMasterLinearity'),
    path('viewAverageLinearity/<int:pk>',viewAverageLinearity,name='viewAverageLinearity'),
    path('viewCommentLinearity/<int:pk>',viewCommentLinearity,name='viewCommentLinearity'),
    path('viewFinalLinearity/<int:pk>',viewFinalLinearity,name='viewFinalLinearity'),
    path('storeLinearity/<int:pk>',storeLinearity,name='storeLinearity'),
    path('storeMasterLinearity/<int:pk>',storeMasterLinearity,name='storeMasterLinearity'),
    path('storeAverageLinearity/<int:pk>',storeAverageLinearity,name='storeAverageLinearity'),
    path('storeAllLinearity/<int:pk>',storeAllLinearity,name='storeAllLinearity'),
    path('storeCommentLinearity/<int:pk>',storeCommentLinearity,name='storeCommentLinearity'),
    path('deleteLinearity/<int:pk>',deleteLinearity,name='deleteLinearity'),

]
