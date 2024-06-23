import { motion } from "framer-motion";
import { Box } from "@chakra-ui/react";

const ShakeBox = ({ children, isError }) => {
  return (
    <motion.div
      animate={isError ? { x: [0, -8, 8, -4, 0] } : { x: 0 }} // Animation keyframes
      transition={{ duration: 0.5 }} // Animation duration
      style={{ display: "inline-block" }} // Ensures the animation works correctly
    >
      <Box>{children}</Box>
    </motion.div>
  );
};

export default ShakeBox;
