export interface Account {
  id: string;
  lnid: string;
  name?: string;
  handle?: string;
  bio?: string;
  github_handle?: string;
  linkedin_handle?: string;
  twitter_handle?: string;
  website?: string;
  avatar_url?: string;
  created_at: string;
  updated_at: string;
}

export interface InstanceAccount {
  account: Account;
  account_id: string;
  instance_id: string;
  permission: string;
  created_at: string;
  updated_at: string;
}
