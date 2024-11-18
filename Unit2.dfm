object Form2: TForm2
  Left = 238
  Top = 165
  Width = 1044
  Height = 540
  Caption = 'Form2'
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'MS Sans Serif'
  Font.Style = []
  OldCreateOrder = False
  PixelsPerInch = 96
  TextHeight = 13
  object DBGrid1: TDBGrid
    Left = 64
    Top = 120
    Width = 537
    Height = 177
    DataSource = DataSource1
    TabOrder = 0
    TitleFont.Charset = DEFAULT_CHARSET
    TitleFont.Color = clWindowText
    TitleFont.Height = -11
    TitleFont.Name = 'MS Sans Serif'
    TitleFont.Style = []
    Columns = <
      item
        Expanded = False
        FieldName = 'idtovar'
        Width = 20
        Visible = True
      end
      item
        Expanded = False
        FieldName = 'tovar'
        Width = 200
        Visible = True
      end
      item
        Expanded = False
        FieldName = 'edizm'
        Width = 100
        Visible = True
      end
      item
        Expanded = False
        FieldName = 'zena'
        Visible = True
      end>
  end
  object DBNavigator1: TDBNavigator
    Left = 248
    Top = 312
    Width = 240
    Height = 25
    DataSource = DataSource1
    TabOrder = 1
  end
  object MySQLDatabase1: TMySQLDatabase
    Connected = True
    DatabaseName = 'bh35910_kis'
    UserName = 'bh35910_student1711'
    UserPassword = 'pgu2023pgu2023'
    Host = '91.219.194.4'
    ConnectOptions = []
    ConnectionCharacterSet = 'utf8'
    Params.Strings = (
      'Port=3306'
      'TIMEOUT=30'
      'DatabaseName=bh35910_kis'
      'UID=bh35910_student1711'
      'PWD=pgu2023pgu2023'
      'Host=91.219.194.4')
    DatasetOptions = []
    Left = 152
    Top = 88
  end
  object MySQLTable1: TMySQLTable
    Database = MySQLDatabase1
    Active = True
    TableName = 'glagolev_tovar'
    Left = 216
    Top = 88
  end
  object DataSource1: TDataSource
    DataSet = MySQLTable1
    Left = 280
    Top = 88
  end
end
