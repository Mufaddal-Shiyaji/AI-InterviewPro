import { Box } from "@mui/material";
import { tokens } from "../../theme";
import Header from "../../components/Header";
import { useTheme } from "@mui/material";

const ResourceRepo = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  return (
    <div>
    <Box m="20px">
      <Header
        title="Resource Repository"
        subtitle="Search for required resources here"
      />
    </Box>
    <Box m='30px'>Enter Resource Repository Here:</Box>
    
    </div>
  );
};

export default ResourceRepo;
