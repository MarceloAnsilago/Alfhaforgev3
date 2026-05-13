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

#import "shell32.dll"
int ShellExecuteW(int hwnd,string lpOperation,string lpFile,string lpParameters,string lpDirectory,int nShowCmd);
#import

string BUTTON_CREATE_NAME   = "AlphaForgeV3.BtnCreateStrategy";
string BUTTON_OPTIMIZE_NAME = "AlphaForgeV3.BtnOptimize";
string BUTTON_OPERATE_NAME  = "AlphaForgeV3.BtnOperate";
string PANEL_NAME           = "AlphaForgeV3.Panel";
string LOG_PANEL_NAME       = "AlphaForgeV3.LogPanel";
string LOG_LABEL_PREFIX     = "AlphaForgeV3.LogLabel.";
string BRIDGE_FILE_NAME     = "AlphaForgeV3_bridge_state.txt";
int TIMER_INTERVAL_MS       = 100;

bool g_operation_enabled = false;
string g_bridge_status = "Aguardando payload do frontend";
string g_bridge_strategy_name = "-";
string g_bridge_magic_number = "-";
string g_bridge_updated_at = "-";
ulong g_last_bridge_poll_ms = 0;
CAlphaForgeOptimizeModal g_optimize_modal;
CAlphaForgeChartTheme g_chart_theme;

string BuildFrontendPath(const string entry_name)
  {
   string root_dir=TerminalInfoString(TERMINAL_DATA_PATH)+"\\MQL5\\Experts\\Advisors\\V3\\Frontend";
   if(entry_name=="")
      return(root_dir);

   return(root_dir+"\\"+entry_name);
  }

bool LaunchFrontendWith(const string executable,const string parameters,const string working_dir)
  {
   int result=ShellExecuteW(0,"open",executable,parameters,working_dir,1);
   return(result>32);
  }

void NotifyFrontendPending()
  {
   string frontend_dir=BuildFrontendPath("");
   string app_path=BuildFrontendPath("app.py");
   if(frontend_dir=="" || app_path=="")
     {
      Print("AlphaForge V3: nao foi possivel resolver o caminho do frontend.");
      return;
     }

   string app_argument="\""+app_path+"\"";
   if(LaunchFrontendWith("pythonw.exe",app_argument,frontend_dir))
     {
      Print("AlphaForge V3: frontend iniciado com pythonw.exe -> ",app_path);
      return;
     }

   if(LaunchFrontendWith("python.exe",app_argument,frontend_dir))
     {
      Print("AlphaForge V3: frontend iniciado com python.exe -> ",app_path);
      return;
     }

   if(LaunchFrontendWith("py.exe","-3 "+app_argument,frontend_dir))
     {
      Print("AlphaForge V3: frontend iniciado com py.exe -> ",app_path);
      return;
     }

   Print("AlphaForge V3: falha ao iniciar o frontend. Verifique Python e customtkinter instalados.");
  }

void UpdateBridgeField(const string key,const string value)
  {
   if(key=="bridge_status")
      g_bridge_status=value;
   else
      if(key=="strategy_name")
         g_bridge_strategy_name=value;
      else
         if(key=="magic_number")
            g_bridge_magic_number=value;
         else
            if(key=="updated_at")
               g_bridge_updated_at=value;
  }

bool CreateLogOverlay()
  {
   if(ObjectFind(0,LOG_PANEL_NAME)<0)
     {
      if(!ObjectCreate(0,LOG_PANEL_NAME,OBJ_RECTANGLE_LABEL,0,0,0))
         return(false);
     }

   ObjectSetInteger(0,LOG_PANEL_NAME,OBJPROP_CORNER,CORNER_LEFT_UPPER);
   ObjectSetInteger(0,LOG_PANEL_NAME,OBJPROP_XDISTANCE,18);
   ObjectSetInteger(0,LOG_PANEL_NAME,OBJPROP_YDISTANCE,86);
   ObjectSetInteger(0,LOG_PANEL_NAME,OBJPROP_XSIZE,360);
   ObjectSetInteger(0,LOG_PANEL_NAME,OBJPROP_YSIZE,108);
   ObjectSetInteger(0,LOG_PANEL_NAME,OBJPROP_BGCOLOR,C'18,27,42');
   ObjectSetInteger(0,LOG_PANEL_NAME,OBJPROP_BORDER_COLOR,C'50,70,100');
   ObjectSetInteger(0,LOG_PANEL_NAME,OBJPROP_COLOR,C'50,70,100');
   ObjectSetInteger(0,LOG_PANEL_NAME,OBJPROP_BACK,false);
   ObjectSetInteger(0,LOG_PANEL_NAME,OBJPROP_SELECTABLE,false);
   ObjectSetInteger(0,LOG_PANEL_NAME,OBJPROP_HIDDEN,true);

   string names[4]=
     {
      LOG_LABEL_PREFIX+"0",
      LOG_LABEL_PREFIX+"1",
      LOG_LABEL_PREFIX+"2",
      LOG_LABEL_PREFIX+"3"
     };
   int y_positions[4]={96,114,132,150};

   for(int i=0;i<4;i++)
     {
      if(ObjectFind(0,names[i])<0)
        {
         if(!ObjectCreate(0,names[i],OBJ_LABEL,0,0,0))
            return(false);
        }

      ObjectSetInteger(0,names[i],OBJPROP_CORNER,CORNER_LEFT_UPPER);
      ObjectSetInteger(0,names[i],OBJPROP_XDISTANCE,28);
      ObjectSetInteger(0,names[i],OBJPROP_YDISTANCE,y_positions[i]);
      ObjectSetInteger(0,names[i],OBJPROP_FONTSIZE,9);
      ObjectSetInteger(0,names[i],OBJPROP_COLOR,C'210,220,235');
      ObjectSetInteger(0,names[i],OBJPROP_SELECTABLE,false);
      ObjectSetInteger(0,names[i],OBJPROP_HIDDEN,true);
      ObjectSetString(0,names[i],OBJPROP_FONT,"Consolas");
     }
   return(true);
  }

void RefreshBridgeOverlay()
  {
   CreateLogOverlay();
   ObjectSetString(0,LOG_LABEL_PREFIX+"0",OBJPROP_TEXT,"AlphaForge V3");
   ObjectSetString(0,LOG_LABEL_PREFIX+"1",OBJPROP_TEXT,"Bridge: "+g_bridge_status);
   ObjectSetString(0,LOG_LABEL_PREFIX+"2",OBJPROP_TEXT,"Strategy: "+g_bridge_strategy_name);
   ObjectSetString(0,LOG_LABEL_PREFIX+"3",OBJPROP_TEXT,"Magic: "+g_bridge_magic_number);
   ChartRedraw();
  }

void SyncFrontendBridge()
  {
   ulong now_ms=GetTickCount64();
   if(now_ms-g_last_bridge_poll_ms<500)
      return;

   g_last_bridge_poll_ms=now_ms;
   int handle=FileOpen(BRIDGE_FILE_NAME,FILE_READ|FILE_TXT|FILE_COMMON|FILE_ANSI);
   if(handle==INVALID_HANDLE)
     {
      g_bridge_status="Aguardando payload do frontend";
      RefreshBridgeOverlay();
      return;
     }

   while(!FileIsEnding(handle))
     {
      string line=FileReadString(handle);
      int delimiter=StringFind(line,"=");
      if(delimiter<=0)
         continue;

      string key=StringSubstr(line,0,delimiter);
      string value=StringSubstr(line,delimiter+1);
      StringTrimLeft(key);
      StringTrimRight(key);
      StringTrimLeft(value);
      StringTrimRight(value);
      UpdateBridgeField(key,value);
     }

   FileClose(handle);
   RefreshBridgeOverlay();
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
   ObjectDelete(0,LOG_PANEL_NAME);
   ObjectDelete(0,LOG_LABEL_PREFIX+"0");
   ObjectDelete(0,LOG_LABEL_PREFIX+"1");
   ObjectDelete(0,LOG_LABEL_PREFIX+"2");
   ObjectDelete(0,LOG_LABEL_PREFIX+"3");
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

   if(!CreateLogOverlay())
     {
      Print("AlphaForge V3: falha ao criar painel de logs.");
      DestroyControlPanel();
      g_chart_theme.RestoreTheme();
      return(INIT_FAILED);
     }

   RefreshBridgeOverlay();

   if(!EventSetMillisecondTimer(TIMER_INTERVAL_MS))
     {
      Print("AlphaForge V3: falha ao iniciar o timer da interface.");
      DestroyControlPanel();
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
   EventKillTimer();
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
   SyncFrontendBridge();

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
      CreateLogOverlay();
      RefreshBridgeOverlay();
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
