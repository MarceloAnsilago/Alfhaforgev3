#ifndef __ALPHAFORGE_V3_OPTIMIZE_MODAL_MQH__
#define __ALPHAFORGE_V3_OPTIMIZE_MODAL_MQH__

#include "..\..\..\Construtor\UI\CEFGuiAliases.mqh"

class CAlphaForgeOptimizeModal : public CEF_CWndCreate
  {
private:
   bool            m_created;
   bool            m_visible;
   int             m_window_index;

   CEF_CWindow     m_window;
   CEF_CTextLabel  m_title;
   CEF_CTextLabel  m_body;
   CEF_CButton     m_close_button;

public:
                     CAlphaForgeOptimizeModal(void) :
                        m_created(false),
                        m_visible(false),
                        m_window_index(-1)
                     {}

   bool CreateIfNeeded(void)
     {
      if(m_created)
         return(true);

      int chart_w=(int)ChartGetInteger(0,CHART_WIDTH_IN_PIXELS,0);
      int chart_h=(int)ChartGetInteger(0,CHART_HEIGHT_IN_PIXELS,0);
      if(chart_w<480)
         chart_w=1280;
      if(chart_h<320)
         chart_h=720;

      const int modal_w=460;
      const int modal_h=220;
      const int pos_x=(chart_w-modal_w)/2;
      const int pos_y=(chart_h-modal_h)/2;

      if(!CreateWindow(m_window,"AlphaForge V3 | Otimizacao",pos_x,pos_y,modal_w,modal_h,true,false,false,false))
         return(false);

      m_window_index=WindowsTotal()-1;
      Hide();

      if(!CreateTextLabel(m_title,"Otimizacao",m_window,m_window_index,24,42,240,26))
         return(false);
      m_title.FontSize(16);
      m_title.LabelColor(C'43,43,43');

      if(!CreateTextLabel(m_body,"Fluxo Easy And Fast GUI validado. A logica de otimizacao sera conectada nas proximas etapas.",m_window,m_window_index,24,80,400,48))
         return(false);
      m_body.FontSize(10);
      m_body.LabelColor(C'91,78,64');

      if(!CreateButton(m_close_button,"Fechar",m_window,m_window_index,24,150,110,false,false,C'39,54,78',C'62,79,101',C'226,114,64',clrWhite,C'18,29,43'))
         return(false);

      CompletedGUI();
      m_created=true;
      return(true);
     }

   bool ShowModal(void)
     {
      if(!CreateIfNeeded())
         return(false);

      Show((uint)m_window_index);
      m_visible=true;
      return(true);
     }

   void HideModal(void)
     {
      if(!m_created)
         return;

      Hide();
      m_visible=false;
     }

   bool IsVisible(void) const
     {
      return(m_visible);
     }

   bool IsCreated(void) const
     {
      return(m_created && m_window_index>=0);
     }

   void Shutdown(void)
     {
      if(!m_created)
         return;

      Destroy();
      m_created=false;
      m_visible=false;
      m_window_index=-1;
     }

   void ChartEvent(const int id,const long &lparam,const double &dparam,const string &sparam)
     {
      if(!IsCreated())
         return;

      CEF_CWndCreate::ChartEvent(id,lparam,dparam,sparam);

      if(!m_visible)
         return;

      if(id==CHARTEVENT_CUSTOM+ON_CLICK_BUTTON && m_close_button.CheckElementName(sparam))
        {
         HideModal();
         return;
        }

      if(id==CHARTEVENT_CUSTOM+ON_WINDOW_CHANGE_XSIZE
         || id==CHARTEVENT_CUSTOM+ON_WINDOW_CHANGE_YSIZE
         || id==CHARTEVENT_CHART_CHANGE)
        {
         // The library keeps the modal alive; we just preserve visibility.
         Show((uint)m_window_index);
        }
     }
  };

#endif // __ALPHAFORGE_V3_OPTIMIZE_MODAL_MQH__
