import { get } from './utils';

export const getRuns = async (orderBy: string, descending: boolean) => {
  console.log(orderBy);
  const runs = await get(
    `${process.env.NEXT_PUBLIC_LAMIN_REST_DB_URL}/run/?order_by=${orderBy}&desc=${descending}`
  );
  return runs;
};

export const getRun = async (
  runId: string,
  orderByFile: string,
  descendingFile: boolean
) => {
  const run = await get(
    `${process.env.NEXT_PUBLIC_LAMIN_REST_DB_URL}/run/${runId}?order_by_file=${orderByFile}&desc_file=${descendingFile}`
  );
  return run;
};
