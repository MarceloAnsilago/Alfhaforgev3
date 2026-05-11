#ifndef __ALPHAFORGE_CHART_THEME_MQH__
#define __ALPHAFORGE_CHART_THEME_MQH__

struct SAlphaForgeChartThemeState
  {
   color background;
   color foreground;
   color grid;
   color candle_bull;
   color candle_bear;
   color chart_up;
   color chart_down;
   color bid;
   color ask;
   color stop_level;
   long  show_grid;
   long  show_ohlc;
   long  chart_mode;
   long  show_bid_line;
   long  show_ask_line;
   long  show_trade_levels;
   long  show_period_sep;
   long  show_object_descr;
   long  show_last_line;
   bool  is_saved;
  };

class CAlphaForgeChartTheme
  {
private:
   long                        m_chart_id;
   SAlphaForgeChartThemeState  m_original_state;

   bool SaveColor(const ENUM_CHART_PROPERTY_INTEGER property,color &target)
     {
      long value=0;
      if(!ChartGetInteger(m_chart_id,property,0,value))
         return(false);

      target=(color)value;
      return(true);
     }

   bool SaveLong(const ENUM_CHART_PROPERTY_INTEGER property,long &target)
     {
      return(ChartGetInteger(m_chart_id,property,0,target));
     }

   bool SetColor(const ENUM_CHART_PROPERTY_INTEGER property,const color value)
     {
      return(ChartSetInteger(m_chart_id,property,value));
     }

   bool SetLong(const ENUM_CHART_PROPERTY_INTEGER property,const long value)
     {
      return(ChartSetInteger(m_chart_id,property,value));
     }

public:
                     CAlphaForgeChartTheme(void):m_chart_id(0)
     {
      ZeroMemory(m_original_state);
      m_original_state.is_saved=false;
     }

   void              SetChartId(const long chart_id)
     {
      m_chart_id=chart_id;
     }

   bool              SaveCurrentTheme()
     {
      SAlphaForgeChartThemeState snapshot;
      ZeroMemory(snapshot);

      if(!SaveColor(CHART_COLOR_BACKGROUND,snapshot.background)) return(false);
      if(!SaveColor(CHART_COLOR_FOREGROUND,snapshot.foreground)) return(false);
      if(!SaveColor(CHART_COLOR_GRID,snapshot.grid)) return(false);
      if(!SaveColor(CHART_COLOR_CANDLE_BULL,snapshot.candle_bull)) return(false);
      if(!SaveColor(CHART_COLOR_CANDLE_BEAR,snapshot.candle_bear)) return(false);
      if(!SaveColor(CHART_COLOR_CHART_UP,snapshot.chart_up)) return(false);
      if(!SaveColor(CHART_COLOR_CHART_DOWN,snapshot.chart_down)) return(false);
      if(!SaveColor(CHART_COLOR_BID,snapshot.bid)) return(false);
      if(!SaveColor(CHART_COLOR_ASK,snapshot.ask)) return(false);
      if(!SaveColor(CHART_COLOR_STOP_LEVEL,snapshot.stop_level)) return(false);

      if(!SaveLong(CHART_SHOW_GRID,snapshot.show_grid)) return(false);
      if(!SaveLong(CHART_SHOW_OHLC,snapshot.show_ohlc)) return(false);
      if(!SaveLong(CHART_MODE,snapshot.chart_mode)) return(false);
      if(!SaveLong(CHART_SHOW_BID_LINE,snapshot.show_bid_line)) return(false);
      if(!SaveLong(CHART_SHOW_ASK_LINE,snapshot.show_ask_line)) return(false);
      if(!SaveLong(CHART_SHOW_TRADE_LEVELS,snapshot.show_trade_levels)) return(false);
      if(!SaveLong(CHART_SHOW_PERIOD_SEP,snapshot.show_period_sep)) return(false);
      if(!SaveLong(CHART_SHOW_OBJECT_DESCR,snapshot.show_object_descr)) return(false);
      if(!SaveLong(CHART_SHOW_LAST_LINE,snapshot.show_last_line)) return(false);

      snapshot.is_saved=true;
      m_original_state=snapshot;
      return(true);
     }

   bool              ApplyAlphaForgeTheme()
     {
      bool success=true;

      success=SetColor(CHART_COLOR_BACKGROUND,C'34,52,78') && success;
      success=SetColor(CHART_COLOR_FOREGROUND,C'210,220,235') && success;
      success=SetColor(CHART_COLOR_GRID,C'48,68,96') && success;
      success=SetColor(CHART_COLOR_CANDLE_BULL,C'65,190,255') && success;
      success=SetColor(CHART_COLOR_CANDLE_BEAR,C'255,90,90') && success;
      success=SetColor(CHART_COLOR_CHART_UP,C'65,190,255') && success;
      success=SetColor(CHART_COLOR_CHART_DOWN,C'255,90,90') && success;
      success=SetColor(CHART_COLOR_BID,C'180,200,230') && success;
      success=SetColor(CHART_COLOR_ASK,C'180,200,230') && success;
      success=SetColor(CHART_COLOR_STOP_LEVEL,C'220,130,35') && success;

      success=SetLong(CHART_SHOW_GRID,true) && success;
      success=SetLong(CHART_SHOW_OHLC,false) && success;
      success=SetLong(CHART_MODE,CHART_CANDLES) && success;
      success=SetLong(CHART_SHOW_BID_LINE,false) && success;
      success=SetLong(CHART_SHOW_ASK_LINE,false) && success;
      success=SetLong(CHART_SHOW_TRADE_LEVELS,false) && success;
      success=SetLong(CHART_SHOW_PERIOD_SEP,false) && success;
      success=SetLong(CHART_SHOW_OBJECT_DESCR,false) && success;
      success=SetLong(CHART_SHOW_LAST_LINE,false) && success;

      ChartRedraw(m_chart_id);
      return(success);
     }

   bool              RefreshThemeDecorations()
     {
      ChartRedraw(m_chart_id);
      return(true);
     }

   bool              RestoreTheme()
     {
      if(!m_original_state.is_saved)
         return(false);

      bool success=true;

      success=SetColor(CHART_COLOR_BACKGROUND,m_original_state.background) && success;
      success=SetColor(CHART_COLOR_FOREGROUND,m_original_state.foreground) && success;
      success=SetColor(CHART_COLOR_GRID,m_original_state.grid) && success;
      success=SetColor(CHART_COLOR_CANDLE_BULL,m_original_state.candle_bull) && success;
      success=SetColor(CHART_COLOR_CANDLE_BEAR,m_original_state.candle_bear) && success;
      success=SetColor(CHART_COLOR_CHART_UP,m_original_state.chart_up) && success;
      success=SetColor(CHART_COLOR_CHART_DOWN,m_original_state.chart_down) && success;
      success=SetColor(CHART_COLOR_BID,m_original_state.bid) && success;
      success=SetColor(CHART_COLOR_ASK,m_original_state.ask) && success;
      success=SetColor(CHART_COLOR_STOP_LEVEL,m_original_state.stop_level) && success;

      success=SetLong(CHART_SHOW_GRID,m_original_state.show_grid) && success;
      success=SetLong(CHART_SHOW_OHLC,m_original_state.show_ohlc) && success;
      success=SetLong(CHART_MODE,m_original_state.chart_mode) && success;
      success=SetLong(CHART_SHOW_BID_LINE,m_original_state.show_bid_line) && success;
      success=SetLong(CHART_SHOW_ASK_LINE,m_original_state.show_ask_line) && success;
      success=SetLong(CHART_SHOW_TRADE_LEVELS,m_original_state.show_trade_levels) && success;
      success=SetLong(CHART_SHOW_PERIOD_SEP,m_original_state.show_period_sep) && success;
      success=SetLong(CHART_SHOW_OBJECT_DESCR,m_original_state.show_object_descr) && success;
      success=SetLong(CHART_SHOW_LAST_LINE,m_original_state.show_last_line) && success;

      ChartRedraw(m_chart_id);
      return(success);
     }
  };

#endif
