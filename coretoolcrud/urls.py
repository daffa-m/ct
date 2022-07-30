
from django.urls import re_path as url
from django.urls import path
from .views import viewGrrXbarr, viewPrintGrrXbarr, viewCommentGrrXbarr, viewFinalGrrXbarr, storeGrrXbarr, storeAllGrrXbarr, storeCommentGrrXbarr, deleteGrrXbarr
from .views import viewCross, viewPrintCross, viewCommentCross, viewFinalCross, storeCross, storeCommentCross, storeAllCross, deleteCross
from .views import viewNested, viewPrintNested, viewCommentNested, viewFinalNested, storeNested, storeCommentNested, storeAllNested, deleteNested
from .views import viewLinearity, viewPrintLinearity, viewAverageLinearity, viewMasterLinearity, viewCommentLinearity, viewFinalLinearity, storeLinearity, storeMasterLinearity, storeAverageLinearity, storeCommentLinearity, storeAllLinearity, deleteLinearity
from .views import viewVxbarr, viewFinalVxbarr, viewCommentVxbarr, viewPrintVxbarr, storeVxbarr, storeCommentVxbarr, storeAllVxbarr, deleteVxbarr, viewAllVxbarr, viewListVxbarr
from .views import viewSbarr, viewFinalSbarr, viewCommentSbarr, viewPrintSbarr, storeSbarr, storeCommentSbarr, storeAllSbarr, deleteSbarr, viewAllSbarr, viewListSbarr
from .views import viewImr, viewFinalImr, viewCommentImr, viewPrintImr, storeImr, storeCommentImr, storeAllImr, deleteImr, viewAllImr, viewListImr
from .views import viewPchart, viewFinalPchart, viewPrintPchart, storePchart, storeAllPchart, viewAllPchart, viewListPchart, deletePchart
from .views import viewNpchart, viewFinalNpchart, viewPrintNpchart, storeNpchart, storeAllNpchart, viewAllNpchart, viewListNpchart, deleteNpchart, viewCommentNpchart, storeCommentNpchart
from .views import viewUchart, viewFinalUchart, viewPrintUchart, storeUchart, storeAllUchart, viewAllUchart, viewListUchart, deleteUchart, viewCommentUchart, storeCommentUchart, viewNsampleUchart, storeNsampleUchart
from .views import viewCchart, viewFinalCchart, viewPrintCchart, storeCchart, storeAllCchart, viewAllCchart, viewListCchart, deleteCchart, viewCommentCchart, storeCommentCchart
from .views import viewStability, viewPrintStability, viewCommentStability, viewFinalStability, viewAllStability, storeStability, storeCommentStability, storeAllStability, deleteStability
from .views import viewKappa, viewPrintKappa, viewFinalKappa, viewAllKappa, storeKappa, storeAllKappa, deleteKappa
from .views import viewKendall, viewPrintKendall, viewFinalKendall, viewAllKendall, storeKendall, storeAllKendall, deleteKendall
from .views import viewMedianr, viewFinalMedianr, viewPrintMedianr, storeMedianr, storeAllMedianr, deleteMedianr, viewAllMedianr, viewListMedianr
# from .views import viewBias, viewPrintBias, viewCommentBias, viewFinalBias, viewAllBias, storeBias, storeCommentBias, storeAllBias, deleteBias
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

    path('viewVxbarr/<int:pkid>/<int:pksurveyid>',viewVxbarr,name='viewVxbarr'),
    path('viewFinalVxbarr/<int:pkid>/<int:pksurveyid>',viewFinalVxbarr,name='viewFinalVxbarr'),
    path('storeVxbarr/<int:pkid>/<int:pksurveyid>',storeVxbarr,name='storeVxbarr'),
    path('viewCommentVxbarr/<int:pkid>/<int:pksurveyid>',viewCommentVxbarr,name='viewCommentVxbarr'),
    path('viewPrintVxbarr/<int:pkid>/<int:pksurveyid>',viewPrintVxbarr,name='viewPrintVxbarr'),
    path('storeCommentVxbarr/<int:pkid>/<int:pksurveyid>',storeCommentVxbarr,name='storeCommentVxbarr'),
    path('storeAllVxbarr/<int:pkid>/<int:pksurveyid>',storeAllVxbarr,name='storeAllVxbarr'),
    path('deleteVxbarr/<int:pkid>/<int:pksurveyid>',deleteVxbarr,name='deleteVxbarr'),
    path('viewAllVxbarr/<int:pkid>/<int:pksurveyid>',viewAllVxbarr,name='viewAllVxbarr'),
    path('viewListVxbarr/<int:pk>',viewListVxbarr,name='viewListVxbarr'),

    path('viewSbarr/<int:pkid>/<int:pksurveyid>',viewSbarr,name='viewSbarr'),
    path('viewFinalSbarr/<int:pkid>/<int:pksurveyid>',viewFinalSbarr,name='viewFinalSbarr'),
    path('storeSbarr/<int:pkid>/<int:pksurveyid>',storeSbarr,name='storeSbarr'),
    path('viewCommentSbarr/<int:pkid>/<int:pksurveyid>',viewCommentSbarr,name='viewCommentSbarr'),
    path('viewPrintSbarr/<int:pkid>/<int:pksurveyid>',viewPrintSbarr,name='viewPrintSbarr'),
    path('storeCommentSbarr/<int:pkid>/<int:pksurveyid>',storeCommentSbarr,name='storeCommentSbarr'),
    path('storeAllSbarr/<int:pkid>/<int:pksurveyid>',storeAllSbarr,name='storeAllSbarr'),
    path('deleteSbarr/<int:pkid>/<int:pksurveyid>',deleteSbarr,name='deleteSbarr'),
    path('viewAllSbarr/<int:pkid>/<int:pksurveyid>',viewAllSbarr,name='viewAllSbarr'),
    path('viewListSbarr/<int:pk>',viewListSbarr,name='viewListSbarr'),

    path('viewImr/<int:pkid>/<int:pksurveyid>',viewImr,name='viewImr'),
    path('viewFinalImr/<int:pkid>/<int:pksurveyid>',viewFinalImr,name='viewFinalImr'),
    path('storeImr/<int:pkid>/<int:pksurveyid>',storeImr,name='storeImr'),
    path('viewCommentImr/<int:pkid>/<int:pksurveyid>',viewCommentImr,name='viewCommentImr'),
    path('viewPrintImr/<int:pkid>/<int:pksurveyid>',viewPrintImr,name='viewPrintImr'),
    path('storeCommentImr/<int:pkid>/<int:pksurveyid>',storeCommentImr,name='storeCommentImr'),
    path('storeAllImr/<int:pkid>/<int:pksurveyid>',storeAllImr,name='storeAllImr'),
    path('deleteImr/<int:pkid>/<int:pksurveyid>',deleteImr,name='deleteImr'),
    path('viewAllImr/<int:pkid>/<int:pksurveyid>',viewAllImr,name='viewAllImr'),
    path('viewListImr/<int:pk>',viewListImr,name='viewListImr'),

    path('viewPchart/<int:pkid>/<int:pksurveyid>',viewPchart,name='viewPchart'),
    path('viewFinalPchart/<int:pkid>/<int:pksurveyid>',viewFinalPchart,name='viewFinalPchart'),
    path('storePchart/<int:pkid>/<int:pksurveyid>',storePchart,name='storePchart'),
    path('viewPrintPchart/<int:pkid>/<int:pksurveyid>',viewPrintPchart,name='viewPrintPchart'),
    path('storeAllPchart/<int:pkid>/<int:pksurveyid>',storeAllPchart,name='storeAllPchart'),
    path('viewAllPchart/<int:pkid>/<int:pksurveyid>',viewAllPchart,name='viewAllPchart'),
    path('viewListPchart/<int:pk>',viewListPchart,name='viewListPchart'),
    path('deletePchart/<int:pkid>/<int:pksurveyid>',deletePchart,name='deletePchart'),

    path('viewNpchart/<int:pkid>/<int:pksurveyid>',viewNpchart,name='viewNpchart'),
    path('viewFinalNpchart/<int:pkid>/<int:pksurveyid>',viewFinalNpchart,name='viewFinalNpchart'),
    path('storeNpchart/<int:pkid>/<int:pksurveyid>',storeNpchart,name='storeNpchart'),
    path('viewPrintNpchart/<int:pkid>/<int:pksurveyid>',viewPrintNpchart,name='viewPrintNpchart'),
    path('storeAllNpchart/<int:pkid>/<int:pksurveyid>',storeAllNpchart,name='storeAllNpchart'),
    path('viewAllNpchart/<int:pkid>/<int:pksurveyid>',viewAllNpchart,name='viewAllNpchart'),
    path('viewListNpchart/<int:pk>',viewListNpchart,name='viewListNpchart'),
    path('deleteNpchart/<int:pkid>/<int:pksurveyid>',deleteNpchart,name='deleteNpchart'),
    path('viewCommentNpchart/<int:pkid>/<int:pksurveyid>',viewCommentNpchart,name='viewCommentNpchart'),
    path('storeCommentNpchart/<int:pkid>/<int:pksurveyid>',storeCommentNpchart,name='storeCommentNpchart'),

    path('viewUchart/<int:pkid>/<int:pksurveyid>',viewUchart,name='viewUchart'),
    path('viewFinalUchart/<int:pkid>/<int:pksurveyid>',viewFinalUchart,name='viewFinalUchart'),
    path('storeUchart/<int:pkid>/<int:pksurveyid>',storeUchart,name='storeUchart'),
    path('viewPrintUchart/<int:pkid>/<int:pksurveyid>',viewPrintUchart,name='viewPrintUchart'),
    path('storeAllUchart/<int:pkid>/<int:pksurveyid>',storeAllUchart,name='storeAllUchart'),
    path('viewAllUchart/<int:pkid>/<int:pksurveyid>',viewAllUchart,name='viewAllUchart'),
    path('viewListUchart/<int:pk>',viewListUchart,name='viewListUchart'),
    path('deleteUchart/<int:pkid>/<int:pksurveyid>',deleteUchart,name='deleteUchart'),
    path('viewCommentUchart/<int:pkid>/<int:pksurveyid>',viewCommentUchart,name='viewCommentUchart'),
    path('storeCommentUchart/<int:pkid>/<int:pksurveyid>',storeCommentUchart,name='storeCommentUchart'),
    path('viewNsampleUchart/<int:pkid>/<int:pksurveyid>',viewNsampleUchart,name='viewNsampleUchart'),
    path('storeNsampleUchart/<int:pkid>/<int:pksurveyid>',storeNsampleUchart,name='storeNsampleUchart'),

    path('viewCchart/<int:pkid>/<int:pksurveyid>',viewCchart,name='viewCchart'),
    path('viewFinalCchart/<int:pkid>/<int:pksurveyid>',viewFinalCchart,name='viewFinalCchart'),
    path('storeCchart/<int:pkid>/<int:pksurveyid>',storeCchart,name='storeCchart'),
    path('viewPrintCchart/<int:pkid>/<int:pksurveyid>',viewPrintCchart,name='viewPrintCchart'),
    path('storeAllCchart/<int:pkid>/<int:pksurveyid>',storeAllCchart,name='storeAllCchart'),
    path('viewAllCchart/<int:pkid>/<int:pksurveyid>',viewAllCchart,name='viewAllCchart'),
    path('viewListCchart/<int:pk>',viewListCchart,name='viewListCchart'),
    path('deleteCchart/<int:pkid>/<int:pksurveyid>',deleteCchart,name='deleteCchart'),
    path('viewCommentCchart/<int:pkid>/<int:pksurveyid>',viewCommentCchart,name='viewCommentCchart'),
    path('storeCommentCchart/<int:pkid>/<int:pksurveyid>',storeCommentCchart,name='storeCommentCchart'),

    path('viewStability/<int:pk>',viewStability,name='viewStability'),
    path('viewPrintStability/<int:pk>',viewPrintStability,name='viewPrintStability'),
    path('viewCommentStability/<int:pk>',viewCommentStability,name='viewCommentStability'),
    path('viewFinalStability/<int:pk>',viewFinalStability,name='viewFinalStability'),
    path('viewAllStability/<int:pk>',viewAllStability,name='viewAllStability'),
    path('storeStability/<int:pk>',storeStability,name='storeStability'),
    path('storeAllStability/<int:pk>',storeAllStability,name='storeAllStability'),
    path('storeCommentStability/<int:pk>',storeCommentStability,name='storeCommentStability'),
    path('deleteStability/<int:pk>',deleteStability,name='deleteStability'),

    path('viewKappa/<int:pk>',viewKappa,name='viewKappa'),
    path('viewPrintKappa/<int:pk>',viewPrintKappa,name='viewPrintKappa'),
    path('viewFinalKappa/<int:pk>',viewFinalKappa,name='viewFinalKappa'),
    path('viewAllKappa/<int:pk>',viewAllKappa,name='viewAllKappa'),
    path('storeKappa/<int:pk>',storeKappa,name='storeKappa'),
    path('storeAllKappa/<int:pk>',storeAllKappa,name='storeAllKappa'),
    path('deleteKappa/<int:pk>',deleteKappa,name='deleteKappa'),

    path('viewKendall/<int:pk>',viewKendall,name='viewKendall'),
    path('viewPrintKendall/<int:pk>',viewPrintKendall,name='viewPrintKendall'),
    path('viewFinalKendall/<int:pk>',viewFinalKendall,name='viewFinalKendall'),
    path('viewAllKendall/<int:pk>',viewAllKendall,name='viewAllKendall'),
    path('storeKendall/<int:pk>',storeKendall,name='storeKendall'),
    path('storeAllKendall/<int:pk>',storeAllKendall,name='storeAllKendall'),
    path('deleteKendall/<int:pk>',deleteKendall,name='deleteKendall'),

    path('viewMedianr/<int:pkid>/<int:pksurveyid>',viewMedianr,name='viewMedianr'),
    path('viewFinalMedianr/<int:pkid>/<int:pksurveyid>',viewFinalMedianr,name='viewFinalMedianr'),
    path('storeMedianr/<int:pkid>/<int:pksurveyid>',storeMedianr,name='storeMedianr'),
    path('viewPrintMedianr/<int:pkid>/<int:pksurveyid>',viewPrintMedianr,name='viewPrintMedianr'),
    path('storeAllMedianr/<int:pkid>/<int:pksurveyid>',storeAllMedianr,name='storeAllMedianr'),
    path('deleteMedianr/<int:pkid>/<int:pksurveyid>',deleteMedianr,name='deleteMedianr'),
    path('viewAllMedianr/<int:pkid>/<int:pksurveyid>',viewAllMedianr,name='viewAllMedianr'),
    path('viewListMedianr/<int:pk>',viewListMedianr,name='viewListMedianr'),

    # path('viewBias/<int:pk>',viewBias,name='viewBias'),
    # path('viewPrintBias/<int:pk>',viewPrintBias,name='viewPrintBias'),
    # path('viewCommentBias/<int:pk>',viewCommentBias,name='viewCommentBias'),
    # path('viewFinalBias/<int:pk>',viewFinalBias,name='viewFinalBias'),
    # path('viewAllBias/<int:pk>',viewAllBias,name='viewAllBias'),
    # path('storeBias/<int:pk>',storeBias,name='storeBias'),
    # path('storeAllBias/<int:pk>',storeAllBias,name='storeAllBias'),
    # path('storeCommentBias/<int:pk>',storeCommentBias,name='storeCommentBias'),
    # path('deleteBias/<int:pk>',deleteBias,name='deleteBias'),


]
