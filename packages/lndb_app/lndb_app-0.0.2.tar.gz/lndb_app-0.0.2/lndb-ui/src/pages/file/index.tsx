import { useEffect, useState } from 'react';

import { getFiles } from '../../services/file';
import { FileListComponent } from '../../ui/file/FileListComponent';
import { Spinner } from '../../ui/utils/Spinner';

function Files() {
  const [files, setFiles] = useState<any>();
  const [orderBy, setOrderBy] = useState('created_at');
  const [descending, setDescending] = useState(true);

  useEffect(() => {
    getFiles(orderBy, descending).then(res => setFiles(res));
  }, [orderBy, descending]);

  if (files) {
    return (
      <FileListComponent
        files={files}
        orderBy={orderBy}
        setOrderBy={setOrderBy}
        descending={descending}
        setDescending={setDescending}
      />
    );
  }

  return <Spinner />;
}

export default Files;
