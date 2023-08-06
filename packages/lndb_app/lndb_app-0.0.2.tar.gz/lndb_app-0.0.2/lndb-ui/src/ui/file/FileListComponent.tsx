import {
  Box,
  Button,
  Card,
  CardBody,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalHeader,
  ModalOverlay,
  Stack,
  StackDivider,
  useDisclosure
} from '@chakra-ui/react';
import { useRouter } from 'next/router';
import { useCallback, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';

import { addFile } from '../../services/file';
import { Container } from '../utils/layout/Container';
import { FileCardList } from './FileCard';

export const FileListComponent = ({
  files,
  orderBy,
  setOrderBy,
  descending,
  setDescending
}: {
  files: any[];
  orderBy: string;
  setOrderBy: any;
  descending: boolean;
  setDescending: any;
}) => {
  return (
    <Container size="lg">
      <DropZone />

      <FileCardList
        files={files}
        orderBy={orderBy}
        setOrderBy={setOrderBy}
        descending={descending}
        setDescending={setDescending}
      />
    </Container>
  );
};

const DropZone = () => {
  const { acceptedFiles, getRootProps, getInputProps } = useDropzone();
  const { isOpen, onOpen, onClose } = useDisclosure();

  useEffect(() => {
    if (acceptedFiles.length > 0 && !isOpen) {
      onOpen();
    }
  }, [acceptedFiles.length]);

  return (
    <Card padding={'3rem'} marginBottom={'3rem'} backgroundColor={'#EDF2F6'}>
      <div {...getRootProps({ className: 'dropzone' })}>
        <input {...getInputProps()} />
        <p>Drag and drop some files here, or click to select files</p>
      </div>
      <UploadFileModal
        acceptedFiles={acceptedFiles}
        isOpen={isOpen}
        onClose={onClose}
      />
    </Card>
  );
};

const UploadFileModal = ({ acceptedFiles, isOpen, onClose }) => {
  const router = useRouter();

  const fileNames = acceptedFiles.map(
    file => `${file.path} - ${file.size} bytes`
  );

  const uploadCallback = useCallback(() => {
    acceptedFiles.forEach(addFile);
    router.reload();
    onClose();
  }, [acceptedFiles]);

  return (
    <Modal isOpen={isOpen} onClose={onClose} size={'4xl'}>
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>Upload files</ModalHeader>
        <ModalCloseButton />
        <ModalBody>
          <Stack spacing={5} margin={'2rem'}>
            <Card>
              <CardBody>
                <Stack divider={<StackDivider />} spacing="4">
                  {fileNames.map((fileName, i) => (
                    <Box key={i}>{fileName}</Box>
                  ))}
                </Stack>
              </CardBody>
            </Card>
          </Stack>
          <Button
            data-test-id="confirm-upload-file-button"
            onClick={() => uploadCallback()}
            marginBottom={'1rem'}
          >
            Confirm
          </Button>
        </ModalBody>
      </ModalContent>
    </Modal>
  );
};
