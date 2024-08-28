import { createRootRoute, Outlet } from "@tanstack/react-router";
import Sidebar from "../components/Sidebar";

export const Route = createRootRoute({
  component: () => (
    <>
      <Sidebar>
        <Outlet />
      </Sidebar>
    </>
  ),
});
