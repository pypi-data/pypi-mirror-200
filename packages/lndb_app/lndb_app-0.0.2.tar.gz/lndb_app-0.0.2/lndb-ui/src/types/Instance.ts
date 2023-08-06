export interface Instance {
  id: string;
  name: string;
  account_id: string;
  storage_id: string;
  db: string;
  schema_str: string;
  description: string;
  public: boolean;
  created_at: string;
  updated_at: string;
  storage: {
    root: string;
  };
  account: {
    id: string;
    handle: string;
  };
}

export interface InstanceWithPermission {
  permission: string;
  instance: Instance;
}

export interface AccountInstance {
  instance: Instance;
  account_id: string;
  instance_id: string;
  permission: string;
  created_at: string;
  updated_at: string;
}

export interface CreateInstanceFields {
  type: 'sqlite' | 'postgres';
  visibility: 'public' | 'private';
  name: string;
  storage: string;
  db: string;
  schema: string[];
  description: string;
}

export interface InstanceLocalSettings {
  owner: string;
  name: string;
  storage: string;
  db: string;
  schema_str: string;
}
