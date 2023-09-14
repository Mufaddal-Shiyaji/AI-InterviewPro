import { Button,Box, IconButton, useTheme, Radio } from "@mui/material";
import { Dialog, DialogTitle, DialogContent, DialogActions, RadioGroup} from '@material-ui/core';
import { useContext, useState} from "react";
import { ColorModeContext, tokens } from "../../theme";
import InputBase from "@mui/material/InputBase";
import LightModeOutlinedIcon from "@mui/icons-material/LightModeOutlined";
import DarkModeOutlinedIcon from "@mui/icons-material/DarkModeOutlined";
import NotificationsOutlinedIcon from "@mui/icons-material/NotificationsOutlined";
import SettingsOutlinedIcon from "@mui/icons-material/SettingsOutlined";
import PersonOutlinedIcon from "@mui/icons-material/PersonOutlined";
import SearchIcon from "@mui/icons-material/Search";


const Topbar = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const colorMode = useContext(ColorModeContext);
  const [open, setOpen] = useState(false);
  const [roomType, setRoomType] = useState('public');

  return (
    <Box display="flex" justifyContent="space-between" p={2}>
      {/* SEARCH BAR */}
      <Box
        display="flex"
        backgroundColor={colors.primary[400]}
        borderRadius="3px"
      >
        <InputBase sx={{ ml: 2, flex: 1 }} placeholder="Search" />
        <IconButton type="button" sx={{ p: 1 }}>
          <SearchIcon />
        </IconButton>
      </Box>

      {/* ICONS */}
      <Box display="flex">

      <Button
          variant="contained"
          color="primary"
          onClick={() => {
            const handleClickOpen = () => {
              setOpen(true);
            };
            const handleClose = () => {
              setOpen(false);
            };

            const handleCreateRoom = () => {
              // Create a room of the specified type (roomType)
              // You can use the roomType state here to determine the selected type
              console.log('Creating room of type:', roomType);
              handleClose(); // Close the dialog
            };

            return (
              <Box>

      <Button
        onClick={handleClickOpen}
        sx={{
          backgroundColor: colors.blueAccent[700],
          color: colors.grey[100],
          fontSize: "14px",
          fontWeight: "bold",
          padding: "10px 20px",
        }}
      >
        Create Room
      </Button>
      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Create Room</DialogTitle>
        <DialogContent>
          <RadioGroup
            name="roomType"
            value={roomType}
            onChange={(event) => setRoomType(event.target.value)}
          >
            <Radio value="public">Public Room</Radio>
            <Radio value="private">Private Room</Radio>
          </RadioGroup>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button color="primary" onClick={handleCreateRoom}>Create Room</Button>
        </DialogActions>
      </Dialog>
    </Box>
            );
          }}
        >
          Create Room
        </Button>

        <IconButton onClick={colorMode.toggleColorMode}>
          {theme.palette.mode === "dark" ? (
            <DarkModeOutlinedIcon />
          ) : (
            <LightModeOutlinedIcon />
          )}
        </IconButton>
        <IconButton>
          <NotificationsOutlinedIcon />
        </IconButton>
        <IconButton>
          <SettingsOutlinedIcon />
        </IconButton>
        <IconButton>
          <PersonOutlinedIcon />
        </IconButton>
      </Box>
    </Box>
  );
};

export default Topbar;
