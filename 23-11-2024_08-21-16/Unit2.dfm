object Form2: TForm2
  Left = 371
  Top = 129
  Width = 1305
  Height = 675
  Caption = #1058#1086#1074#1072#1088#1099
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'MS Sans Serif'
  Font.Style = []
  OldCreateOrder = False
  PixelsPerInch = 96
  TextHeight = 13
  object Label1: TLabel
    Left = 200
    Top = 32
    Width = 32
    Height = 13
    Caption = 'Label1'
  end
  object Label2: TLabel
    Left = 560
    Top = 32
    Width = 32
    Height = 13
    Caption = 'Label1'
  end
  object Label3: TLabel
    Left = 936
    Top = 32
    Width = 32
    Height = 13
    Caption = 'Label1'
  end
  object DBGrid1: TDBGrid
    Left = 96
    Top = 208
    Width = 1033
    Height = 201
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
        Visible = True
      end
      item
        Expanded = False
        FieldName = 'tovar'
        Visible = True
      end
      item
        Expanded = False
        FieldName = 'edizm'
        Visible = True
      end
      item
        Expanded = False
        FieldName = 'zena'
        Width = 566
        Visible = True
      end>
  end
  object DBNavigator1: TDBNavigator
    Left = 96
    Top = 424
    Width = 1030
    Height = 25
    DataSource = DataSource1
    TabOrder = 1
  end
  object DBEdit1: TDBEdit
    Left = 96
    Top = 64
    Width = 289
    Height = 21
    DataField = 'tovar'
    DataSource = DataSource1
    TabOrder = 2
  end
  object DBEdit2: TDBEdit
    Left = 784
    Top = 64
    Width = 337
    Height = 21
    DataField = 'zena'
    DataSource = DataSource1
    TabOrder = 3
  end
  object DBEdit3: TDBEdit
    Left = 448
    Top = 64
    Width = 289
    Height = 21
    DataField = 'edizm'
    DataSource = DataSource1
    TabOrder = 4
  end
  object MySQLDatabase1: TMySQLDatabase
    Connected = True
    DatabaseName = 'bh35910_kis'
    UserName = 'bh35910_student1711'
    UserPassword = 'pgu2023pgu2023'
    Host = '91.219.194.4'
    ConnectOptions = []
    ConnectionCharacterSet = 'latin1'
    Params.Strings = (
      'Port=3306'
      'TIMEOUT=30'
      'DatabaseName=bh35910_kis'
      'UID=bh35910_student1711'
      'PWD=pgu2023pgu2023'
      'Host=91.219.194.4')
    DatasetOptions = []
    Left = 96
    Top = 160
  end
  object MySQLTable1: TMySQLTable
    Database = MySQLDatabase1
    Active = True
    TableName = 'arharov_tovar'
    Left = 192
    Top = 160
  end
  object DataSource1: TDataSource
    DataSet = MySQLTable1
    Left = 280
    Top = 160
  end
end
