export const handleData = <DataType>(data: DataType) => {
  return {
    error: null,
    data
  };
};

export const handleError = <ErrorType>(error: ErrorType) => {
  return {
    error: JSON.stringify(error),
    data: null
  };
};
