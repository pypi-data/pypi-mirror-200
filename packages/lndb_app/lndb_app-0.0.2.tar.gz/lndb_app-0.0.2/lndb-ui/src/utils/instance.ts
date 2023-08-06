import { Instance } from '../types/Instance';
import { getPostgresHost } from './string';

export const getInstanceDBHost = (instance: Instance): string => {
  if (getInstanceDialect(instance) === 'sqlite') {
    const storageRoot = instance.storage.root;
    const sqliteFile = instance.name + '.lndb';
    return storageRoot + '/' + sqliteFile;
  } else {
    return getPostgresHost(instance.db);
  }
};

export const getInstanceDialect = (instance: Instance): string => {
  const connectionString = instance.db;
  if (!connectionString) {
    return 'sqlite';
  } else {
    return 'postgres';
  }
};

export const getSchemaModules = (instance: Instance): string => {
  const schemaString = instance.schema_str;
  return !schemaString ? 'core' : 'core,' + schemaString;
};
