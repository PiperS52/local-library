import Box from '@mui/material/Box';
import styles from './styles.module.scss';
import Card from '@mui/material/Card';
import Grid from '@mui/material/Grid2';
import { CardResult } from '../CardResult';

import { BookWishlistItem } from '../../services/wishlists/types';

export const WishlistsGrid: React.FC<{
  bookWishlists: BookWishlistItem[];
}> = ({ bookWishlists }) => {
  return (
    <>
      <Box sx={{ flexGrow: 1, padding: 2 }}>
        <Grid container spacing={2}>
          {bookWishlists.map((bookWishlist, index) => (
            <Grid
              size={{ xs: 12, sm: 6, md: 4 }} // 3 per row on md and up, 2 per row on sm, 1 per row on xs
              key={`${bookWishlist.id}-${index}`}
            >
              <CardResult
                title={bookWishlist.title}
                authors={bookWishlist.authors}
                publicationYear={bookWishlist.publicationYear}
                isbn={bookWishlist.isbn}
              />
            </Grid>
          ))}
          {bookWishlists.length === 2 && (
            <Grid size={{ xs: 12, sm: 6, md: 4 }}>
              <Card
                className={styles.card}
                variant="outlined"
                sx={{
                  border: 'none',
                  boxShadow: 'none',
                  background: 'transparent',
                }}
              />{' '}
            </Grid>
          )}
        </Grid>
      </Box>
    </>
  );
};
