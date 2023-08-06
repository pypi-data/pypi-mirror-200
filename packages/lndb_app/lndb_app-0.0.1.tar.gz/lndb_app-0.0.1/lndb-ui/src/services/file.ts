import { get } from './utils';

export const getFiles = async (orderBy: string, descending: boolean) => {
  const runs = await get(
    `${process.env.NEXT_PUBLIC_LAMIN_REST_DB_URL}/file/?order_by=${orderBy}&desc=${descending}`
  );
  return runs;
};

export const getFile = async (fileId: string) => {
  const run = await get(
    `${process.env.NEXT_PUBLIC_LAMIN_REST_DB_URL}/file/${fileId}`
  );
  return run;
};

export const addFile = async (file: any) => {
  console.log('*******', file.name, file);
  const formData = new FormData();
  formData.append('uploadFile', file, file.name);
  const options = {
    method: 'POST',
    body: formData
  };
  fetch(`${process.env.NEXT_PUBLIC_LAMIN_REST_DB_URL}/file/add`, options)
    .then(response => response.json())
    .then(function (response) {
      console.log('response');
      console.log(response);
    });
};
