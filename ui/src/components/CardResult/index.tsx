import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import { Typography } from '@mui/material';
import styles from './styles.module.scss';

export const CardResult: React.FC<{
  title: string;
  authors: string;
  publicationYear: string;
  isbn: string;
}> = ({ title, authors, publicationYear, isbn }) => {
  return (
    <>
      <Card className={styles.card} variant="outlined">
        <CardContent>
          <Typography variant="h6" color="text.primary">
            {title}
          </Typography>
          <p>{authors}</p>
          <p>Publication year: {publicationYear}</p>
          <p>ISBN: {isbn}</p>
        </CardContent>
      </Card>
    </>
  );
};
