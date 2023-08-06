export const getPostgresHost = (connectionString: string): string => {
  return connectionString.split('@')[1];
};

export const prettifyDatetimeString = (datetimeString: string): string => {
  const date = new Date(datetimeString);
  return date.toLocaleString();
};
