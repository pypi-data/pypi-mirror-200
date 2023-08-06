import { TableSchema } from './Table';

//export interface InstanceSchema {
//  key: string;
//  tables: Tables;
//}

export interface InstanceSchema {
  [schemaName: string]: string[]
}

export interface Tables {
  [key: string]: TableSchema;
}
