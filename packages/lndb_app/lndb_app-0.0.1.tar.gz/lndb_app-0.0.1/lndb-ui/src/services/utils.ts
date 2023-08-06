export const get = async (url: string) => {
  const headers = {
    accept: 'application/json'
  };
  const res = await fetch(url, { headers });
  return await res.json();
};
