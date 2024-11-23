object Form5: TForm5
  Left = 203
  Top = 132
  Width = 1305
  Height = 675
  Caption = 'TovarForm'
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'MS Sans Serif'
  Font.Style = []
  Menu = MainMenu1
  OldCreateOrder = False
  PixelsPerInch = 96
  TextHeight = 13
  object Button1: TButton
    Left = 32
    Top = 24
    Width = 129
    Height = 129
    Caption = #1058#1086#1074#1072#1088#1099
    TabOrder = 0
    OnClick = Button1Click
  end
  object Button2: TButton
    Left = 240
    Top = 24
    Width = 121
    Height = 129
    Caption = #1055#1086#1089#1090#1072#1074#1097#1080#1082#1080
    TabOrder = 1
    OnClick = Button2Click
  end
  object Button4: TButton
    Left = 448
    Top = 24
    Width = 129
    Height = 129
    Caption = #1055#1088#1080#1093#1086#1076
    TabOrder = 2
    OnClick = TPrihodClick
  end
  object Button3: TButton
    Left = 32
    Top = 224
    Width = 249
    Height = 145
    Caption = #1047#1072#1087#1088#1086#1089#1099
    TabOrder = 3
    OnClick = Button3Click
  end
  object MainMenu1: TMainMenu
    Left = 8
    Top = 65528
    object cb1: TMenuItem
      Caption = #1057#1080#1089#1090#1077#1084#1072
      object N3: TMenuItem
        Caption = #1053#1072#1089#1090#1088#1086#1081#1082#1080
      end
      object N4: TMenuItem
        Caption = #1042#1099#1093#1086#1076
      end
    end
    object N1: TMenuItem
      Caption = #1041#1072#1079#1072' '#1076#1072#1085#1085#1099#1093
      object N5: TMenuItem
        Caption = #1058#1086#1074#1072#1088#1099
        OnClick = N5Click
      end
      object N6: TMenuItem
        Caption = #1055#1086#1089#1090#1072#1074#1097#1080#1082#1080
        OnClick = N6Click
      end
      object N8: TMenuItem
        Caption = #1055#1088#1080#1093#1086#1076
        OnClick = N8Click
      end
    end
    object N2: TMenuItem
      Caption = #1057#1087#1088#1072#1074#1082#1072
      object N7: TMenuItem
        Caption = #1054' '#1087#1088#1086#1075#1088#1072#1084#1084#1077
      end
      object N9: TMenuItem
        Caption = #1055#1086#1084#1086#1097#1100
      end
    end
  end
end
