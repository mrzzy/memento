
/*
 * Memento
 * Frontend 
 * API Client - Tests
*/

import API from "./API";
import assert from "assert";

describe("API", () => {
    const api = new API(); 
    let orgId, userId;

    // create required objects for testing
    describe("#post(type, params)", () => {
        it("should create organisation", async () => {
            const response = await api.post("org", {
                name: "James Bakery"
            });
            assert(response.id);
            orgId = response.id
            
        });
        it("should create user", async () => {
            const response = await api.post("user", {
                "name": "joel",
                "password": "P@$$w0rd",
                "email": "joel@gmail.com",
                "orgId": orgId
            })
            assert(response.id);
            userId = response.id;
        });
    });

    // authentication
    describe("#login(username, password)", () => {
        it("show perform login", async () => {
            const hasLogin = await api.login("joel@gmail.com", "P@$$w0rd");
            assert(hasLogin);
            assert(api.state.refreshToken);
        });
    });
    
    describe("#authCheck()", () => {
        it("show perform auth token check", async () => {
            const loggedInUserId = await api.authCheck();
            assert(loggedInUserId == userId);
        });
    });
    
    describe("#refresh(username, password)", () => {
        it("show perform access token refresh", async () => {
            const hasRefresh = await api.refresh();
            assert(hasRefresh);
        });
    });
    
    
    // test crud on org api
    describe("#query(type, params)", () => {
        it("should get orgs ids", async () => {
            const orgIds = await api.query("org", {"limit": 1, "skip": 0});
            assert(orgIds.length === 1);
        });
    });
    describe("#get(type, id)", () => {
        it("should get organisation", async () => {
            const orgIds = await api.query("org", {"limit": 1, "skip": 0});
            const org = await api.get("org", orgIds[0]);
            assert(org.name === "James Bakery");
        });
    });
    describe("#update(type, id, params)", () => {
        it("should update organisation", async () => {
            const orgIds = await api.query("org", {"limit": 1, "skip": 0});
            const response = await api.update("org", orgIds[0], {
                name: "John's Bakery"
            });
            assert(response.success);
        });
    });
    
    // cleanup
    describe("#delete(type,id)", () => {
        it("should delete organisation", async() => {
            const orgIds = await api.query("org", {"limit": 1, "skip": 0});
            const response = await api.delete("org", orgIds[0]);
            assert(response.success);
        });
    });
    
    // logout
    describe("#logout()", () => {
        it("should failed as unauthorised", async() => {
            api.logout();
            var hasError = false;
            try {
                await api.get("org", 0);
            } catch(error) {
                hasError = true;
            }
            assert(hasError);
        });
    });
});
