import { get } from './utils';

export const getCurrentInstance = async () => {
  const instance = await get(
    `${process.env.NEXT_PUBLIC_LAMIN_REST_DB_URL}/instance/`
  );
  return instance;
};
