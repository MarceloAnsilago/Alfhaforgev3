//+------------------------------------------------------------------+
//|                                                 AlphaForgeV3.mq5 |
//|                                  Copyright 2026, MetaQuotes Ltd. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2026, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"

#include "AlphaForgeOptimizeModal.mqh"
#include "Theme/ChartTheme.mqh"

string BUTTON_CREATE_NAME   = "AlphaForgeV3.BtnCreateStrategy";
string BUTTON_OPTIMIZE_NAME = "AlphaForgeV3.BtnOptimize";
string BUTTON_OPERATE_NAME  = "AlphaForgeV3.BtnOperate";
string PANEL_NAME           = "AlphaForgeV3.Panel";

bool g_operation_enabled = false;
CAlphaForgeOptimizeModal g_optimize_modal;
CAlphaForgeChartTheme g_chart_theme;

void NotifyFrontendPending()
  {
   Print("Frontend ainda nao implementado");
  }

bool CreateButtonObject(const string name,const string text,const int x,const int y,const int width,const color back_color)
  {
   if(ObjectFind(0,name)<0)
     {
      if(!ObjectCreate(0,name,OBJ_BUTTON,0,0,0))
         return(false);
     }

   ObjectSetInteger(0,name,OBJPROP_CORNER,CORNER_LEFT_UPPER);
   ObjectSetInteger(0,name,OBJPROP_XDISTANCE,x);
   ObjectSetInteger(0,name,OBJPROP_YDISTANCE,y);
   ObjectSetInteger(0,name,OBJPROP_XSIZE,width);
   ObjectSetInteger(0,name,OBJPROP_YSIZE,34);
   ObjectSetInteger(0,name,OBJPROP_FONTSIZE,10);
   ObjectSetInteger(0,name,OBJPROP_COLOR,C'210,220,235');
   ObjectSetInteger(0,name,OBJPROP_BGCOLOR,back_color);
   ObjectSetInteger(0,name,OBJPROP_BORDER_COLOR,C'50,70,100');
   ObjectSetInteger(0,name,OBJPROP_SELECTABLE,false);
   ObjectSetInteger(0,name,OBJPROP_HIDDEN,true);
   ObjectSetString(0,name,OBJPROP_TEXT,text);
   return(true);
  }

bool CreateBackgroundPanel()
  {
   if(ObjectFind(0,PANEL_NAME)<0)
     {
      if(!ObjectCreate(0,PANEL_NAME,OBJ_RECTANGLE_LABEL,0,0,0))
         return(false);
     }

   ObjectSetInteger(0,PANEL_NAME,OBJPROP_CORNER,CORNER_LEFT_UPPER);
   ObjectSetInteger(0,PANEL_NAME,OBJPROP_XDISTANCE,18);
   ObjectSetInteger(0,PANEL_NAME,OBJPROP_YDISTANCE,18);
   ObjectSetInteger(0,PANEL_NAME,OBJPROP_XSIZE,458);
   ObjectSetInteger(0,PANEL_NAME,OBJPROP_YSIZE,56);
   ObjectSetInteger(0,PANEL_NAME,OBJPROP_BGCOLOR,C'24,36,58');
   ObjectSetInteger(0,PANEL_NAME,OBJPROP_BORDER_COLOR,C'50,70,100');
   ObjectSetInteger(0,PANEL_NAME,OBJPROP_COLOR,C'50,70,100');
   ObjectSetInteger(0,PANEL_NAME,OBJPROP_BACK,false);
   ObjectSetInteger(0,PANEL_NAME,OBJPROP_SELECTABLE,false);
   ObjectSetInteger(0,PANEL_NAME,OBJPROP_HIDDEN,true);
   return(true);
  }

bool CreateControlPanel()
  {
   if(!CreateBackgroundPanel())
      return(false);
   if(!CreateButtonObject(BUTTON_CREATE_NAME,"Criar Estrategia",28,29,140,C'45,110,255'))
      return(false);
   if(!CreateButtonObject(BUTTON_OPTIMIZE_NAME,"Otimizar",176,29,128,C'0,150,170'))
      return(false);
   if(!CreateButtonObject(BUTTON_OPERATE_NAME,"Operar",312,29,148,C'220,130,35'))
      return(false);

   ChartRedraw();
   return(true);
  }

void DestroyControlPanel()
  {
   ObjectDelete(0,BUTTON_CREATE_NAME);
   ObjectDelete(0,BUTTON_OPTIMIZE_NAME);
   ObjectDelete(0,BUTTON_OPERATE_NAME);
   ObjectDelete(0,PANEL_NAME);
  }
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
   g_chart_theme.SetChartId(ChartID());

   if(!g_chart_theme.SaveCurrentTheme())
     {
      Print("AlphaForge V3: falha ao salvar o tema original do grafico.");
      return(INIT_FAILED);
     }

   if(!g_chart_theme.ApplyAlphaForgeTheme())
     {
      Print("AlphaForge V3: falha ao aplicar o tema visual.");
      g_chart_theme.RestoreTheme();
      return(INIT_FAILED);
     }

   if(!CreateControlPanel())
     {
      Print("AlphaForge V3: falha ao criar o painel inicial.");
      g_chart_theme.RestoreTheme();
      return(INIT_FAILED);
     }

   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   DestroyControlPanel();
   g_optimize_modal.Shutdown();
   g_chart_theme.RestoreTheme();
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
  }
//+------------------------------------------------------------------+
//| Timer                                                            |
//+------------------------------------------------------------------+
void OnTimer()
  {
   if(g_optimize_modal.IsCreated())
      g_optimize_modal.OnTimerEvent();
  }
//+------------------------------------------------------------------+
//| Chart event                                                      |
//+------------------------------------------------------------------+
void OnChartEvent(const int id,const long &lparam,const double &dparam,const string &sparam)
  {
   if(g_optimize_modal.IsCreated())
      g_optimize_modal.ChartEvent(id,lparam,dparam,sparam);

   if(id==CHARTEVENT_CHART_CHANGE)
     {
      g_chart_theme.RefreshThemeDecorations();
      CreateControlPanel();
      return;
     }

   if(id!=CHARTEVENT_OBJECT_CLICK)
      return;

   if(sparam==BUTTON_CREATE_NAME)
     {
      NotifyFrontendPending();
      return;
     }

   if(sparam==BUTTON_OPTIMIZE_NAME)
     {
      g_optimize_modal.ShowModal();
      return;
     }

   if(sparam==BUTTON_OPERATE_NAME)
     {
      g_operation_enabled=!g_operation_enabled;
      Print(g_operation_enabled ? "Modo operacional ativado" : "Modo operacional desativado");
      return;
     }
  }
