export interface Table {
  schema: TableSchema;
  rows: Row[];
}

export interface TableSchema {
  key: string;
  foreign_keys: string[][];
  primary_keys: string[];
  columns: {
    [key: string]: Column;
  };
}

export interface Column {
  key: string;
  type: string;
  foreign_keys: string[][];
  primary_key: boolean;
  nullable: boolean;
  default: any;
}

export interface Row {
  [key: string]: any;
}
