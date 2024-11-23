object TPrihod: TTPrihod
  Left = 405
  Top = 298
  Width = 1305
  Height = 675
  Caption = #1055#1088#1080#1093#1086#1076
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
    Left = 40
    Top = 120
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
        FieldName = 'idprihod'
        Visible = True
      end
      item
        Expanded = False
        FieldName = 'idtovar'
        Visible = True
      end
      item
        Expanded = False
        FieldName = 'datPrih'
        Visible = True
      end
      item
        Expanded = False
        FieldName = 'kolvo'
        Visible = True
      end
      item
        Expanded = False
        FieldName = 'namepostav'
        Visible = True
      end
      item
        Expanded = False
        FieldName = 'nametovar'
        Width = 626
        Visible = True
      end>
  end
  object DBNavigator1: TDBNavigator
    Left = 40
    Top = 336
    Width = 1030
    Height = 25
    DataSource = DataSource1
    TabOrder = 1
  end
  object DBEdit1: TDBEdit
    Left = 88
    Top = 56
    Width = 121
    Height = 21
    DataField = 'datPrih'
    DataSource = DataSource1
    TabOrder = 2
  end
  object DBEdit2: TDBEdit
    Left = 240
    Top = 56
    Width = 121
    Height = 21
    DataField = 'kolvo'
    DataSource = DataSource1
    TabOrder = 3
  end
  object DBLookupComboBox1: TDBLookupComboBox
    Left = 400
    Top = 56
    Width = 145
    Height = 21
    DataField = 'nametovar'
    DataSource = DataSource1
    ListField = 'tovar'
    TabOrder = 4
  end
  object DBLookupComboBox2: TDBLookupComboBox
    Left = 592
    Top = 56
    Width = 145
    Height = 21
    DataField = 'idpostav'
    DataSource = DataSource1
    KeyField = 'id_postav'
    ListField = 'postav'
    ListSource = DataSource2
    TabOrder = 5
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
    Left = 336
    Top = 216
  end
  object MySQLTable1: TMySQLTable
    Database = MySQLDatabase1
    Active = True
    TableName = 'arharov_prihod'
    Left = 432
    Top = 216
    object MySQLTable1idprihod: TAutoIncField
      FieldName = 'idprihod'
      Origin = 'arharov_prihod.idprihod'
    end
    object MySQLTable1idtovar: TIntegerField
      FieldName = 'idtovar'
      Origin = 'arharov_prihod.idtovar'
    end
    object MySQLTable1datPrih: TDateField
      FieldName = 'datPrih'
      Origin = 'arharov_prihod.datPrih'
    end
    object MySQLTable1kolvo: TIntegerField
      FieldName = 'kolvo'
      Origin = 'arharov_prihod.kolvo'
    end
    object MySQLTable1idpostav: TIntegerField
      FieldName = 'idpostav'
      Origin = 'arharov_prihod.idpostav'
    end
    object MySQLTable1namepostav: TStringField
      FieldKind = fkLookup
      FieldName = 'namepostav'
      LookupDataSet = MySQLTable2
      LookupKeyFields = 'id_postav'
      LookupResultField = 'postav'
      KeyFields = 'idpostav'
      Lookup = True
    end
    object MySQLTable1nametovar: TStringField
      FieldKind = fkLookup
      FieldName = 'nametovar'
      LookupDataSet = MySQLTable3
      LookupKeyFields = 'idtovar'
      LookupResultField = 'tovar'
      KeyFields = 'idtovar'
      Lookup = True
    end
  end
  object DataSource1: TDataSource
    DataSet = MySQLTable1
    Left = 520
    Top = 216
  end
  object MySQLTable2: TMySQLTable
    Database = MySQLDatabase1
    Active = True
    TableName = 'arharov_postav'
    Left = 744
    Top = 24
  end
  object DataSource2: TDataSource
    DataSet = MySQLTable2
    Left = 744
    Top = 80
  end
  object MySQLTable3: TMySQLTable
    Database = MySQLDatabase1
    Active = True
    TableName = 'arharov_tovar'
    Left = 464
    Top = 16
  end
  object DataSource3: TDataSource
    DataSet = MySQLTable3
    Left = 424
    Top = 16
  end
end
