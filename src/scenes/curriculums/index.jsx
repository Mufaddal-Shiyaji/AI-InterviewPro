import { Box, Card, CardContent, CardMedia, Typography} from "@mui/material";
import Header from "../../components/Header";
import { spacing } from '@mui/system';


const CurriculumCard = ({ curriculum }) => {
  const { image, name, status, hours } = curriculum;

  return (
    <Card>
      <CardMedia
        image={image}
        title="Curriculum Image"
        height="150px"
      />
      <CardContent>
        <Typography variant="h5" gutterBottom>
          {name}
        </Typography>
        <Typography>
          {status} • {hours} hours
        </Typography>
      </CardContent>
    </Card>
  );
};

const curriculums = [
  {
    image: "../../assets/image1.jpeg",
    name: "Data Structures",
    status: "Completed",
    hours: 10,
  },
  {
    image: "image2.png",
    name: "DBMS",
    status: "Pending",
    hours: 8,
  },
  {
    image: "image3.png",
    name: "Discrete Structures",
    status: "In Progress",
    hours: 9,
  },
];



const Curriculums= () => {


  return (
    <Box m="20px">
      <Header title="MY CURRICULUMS" subtitle="Access all ongoing/developed curriculums here" />
      {curriculums.map((curriculum) => (
        <CurriculumCard curriculum={curriculum} />
      ))}
    </Box>
  );
};

const styles = {
  card: {
    margin: spacing(8),
  },
};

export default Curriculums;
