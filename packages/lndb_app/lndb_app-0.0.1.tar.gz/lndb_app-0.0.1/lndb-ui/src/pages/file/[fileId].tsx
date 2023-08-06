import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

import { getFile } from '../../services/file';
import { FileComponent } from '../../ui/file/FileComponent';
import { FileComponentTabName } from '../../ui/file/FileComponentBody';
import { Spinner } from '../../ui/utils/Spinner';

function File() {
  const router = useRouter();

  const [file, setFile] = useState<any>();

  const { fileId, tab } = router.query;

  useEffect(() => {
    getFile(fileId as string).then(res => setFile(res));
  }, []);

  if (file) {
    return <FileComponent tab={tab as FileComponentTabName} file={file} />;
  }

  return <Spinner />;
}

export default File;
