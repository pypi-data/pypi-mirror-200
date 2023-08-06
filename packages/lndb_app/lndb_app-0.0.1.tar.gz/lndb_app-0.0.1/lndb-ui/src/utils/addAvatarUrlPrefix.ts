export const addAvatarUrlPrefix = (avatar_url: string) => {
  return `${process.env.NEXT_PUBLIC_SUPABASE_URL}/storage/v1/object/public/storage-user-hub/${avatar_url}`;
};
