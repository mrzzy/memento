/*
 * Memento
 * Frontend 
 * API Client
*/

import assert from "assert";
import fetch from "cross-fetch";
import dotenv from "dotenv";
import Cookie from "js-cookie";

// defines an api client to interface with the backend api
export default class API {
    // constructs client to interface with the api
    constructor() {
        // load config from environment 
        dotenv.config();
        this.apiHost = process.env.BACKEND_API_HOST || "memento.mrzzy.co";
        this.apiVersion = 1
        this.protocol = process.env.BACKEND_API_PROTOCOL || "https";
        // check protocol support
        assert(this.protocol === "http" || this.protocol === "https");
        // build api root url from configuration
        this.apiRoot = `${this.protocol}://${this.apiHost}/api/v${this.apiVersion}`

        // object state
        this.stateCookieName = "memento-api-obj-state";
        // try to load state form cookie
        this.state = Cookie.getJSON(this.stateCookieName);
        if(this.state == null) {
            this.state = { 
                "refreshToken": null,
                "accessToken": null,
            };
        }

        // build map of available api routes
        this.apiMap = {
            "auth": ["login", "check", "refresh"],
            "identity": 
            [ "org", "user", "team", "team/assign", "manage", "role", "rolebind"],
            "assignment": ["task", "event", "assign"],
            "notify": ["notify", "channel"],
        };
    }

    /* utils */
    // convert the given set of url param to url param string
    // returns the url param string 
    convertUrl(params) {
        return "?" + Object.entries(params)
            .map(([key, value]) => `${key}=${value}`).join("&");
    }

    // returns true if given type is supported, otherwise false
    supports(type)  {
        for(let [service, types] of Object.entries(this.apiMap)) {
            if(types.includes(type) ) {
                // don't support calling auth api directly
                if(service === "auth") return false; 
                return true;
            }
        }
        return false;
    }

    // build object url 
    // type - type of object to build. Must be supported
    objectUrl(type) {
        // map type to service
        for(let [service, types] of Object.entries(this.apiMap)) {
            if(types.includes(type)) {
                // found matching service & type in api map 
                const objectUrl = `${this.apiRoot}/${service}/${type}`;
                return objectUrl;
            }
        }
    
        throw `API: Unknown api type: ${type}`;
    }

    // set the values in the given valueMap dict to the object state
    // commits the state into a cookie for persistence
    setState(valueMap) {
        for(let [key, value] of Object.entries(valueMap)) {
            this.state[key] = value;
        }
    
        // store object state for 14 days
        Cookie.set(this.stateCookieName, this.state, { "expires": 14 });
    }
    
    // checks the given response for errors
    // if detected, throws and exception detailing the error
    async checkResponse(response) {
        if(response.status != 200) {
            const body = await response.text();
            throw `FATAL: API call failed with status code: ${response.status}, response: ${body}`;
        }
    }

    /* authentication */
    // perform authentication with the given user credentials
    // should be called before making most API calls
    // username - username of the user 
    // password - password of the user
    // returns true if login success, false otherwise
    async login(username, password) {
        var response = await fetch(this.objectUrl("login"),{
            method: "POST",
            mode: "cors",
            cache: "no-cache",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ "username": username, "password": password})
        });
        await this.checkResponse(response);
        response = await response.json();

        if(response.refreshToken != null) {
            this.setState({"refreshToken": response.refreshToken});
            return true;
        } else {
            return false;
        }
    }
    
    // perform logout by removing session tokens (access & refresh)
    // does nothing if not already logged in
    logout() {
        this.setState({
            "accessToken": null,
            "refreshToken": null
        });
    }

    // check if api is currently authenticated with the api server.
    // Returns the user id of the user that we are logged in as 
    // or null if not logged in.
    async authCheck() {
        var response = await fetch(this.objectUrl("check"),{
            method: "GET",
            mode: "cors",
            cache: "no-cache",
            headers: {
                "Authorization": `Bearer ${this.state.refreshToken}`
            }
        });
        await this.checkResponse(response);
        response = await response.json();
        
        return (response.success === true) ? response.userId: null;
    }
    
    // attempts to refresh the access token using the refreshToken
    // only refreshes the access token once it expires
    // if no refreshToken is available does nothing
    // return true if refresh success, false otherwise
    async refresh() {
        // check if has refreshToken to perfrom refresh 
        if(this.state.refreshToken == null) return;
        // check access token has expired
        if(this.state.accessToken != null) return;
        // make refresh request
        var response = await fetch(this.objectUrl("refresh"), {
            method: "GET",
            mode: "cors",
            cache: "no-cache",
            headers: {
                "Authorization": `Bearer ${this.state.refreshToken}`
            }
        });
        await this.checkResponse(response);
        response = await response.json();
        
        if(response.accessToken != null) {
            this.setState({"accessToken": response.accessToken});
            // auto expire access token
            setTimeout(() => {
                this.setState({"accessToken": null});
            }, 4 * 60 * 1000);
            return true;
        } else {
            return false;
        }
    }
    
    // attach token to authenticate with the api server to the given request
    // uses access token if available, request token if available, otherwise does nothing
    // returns the given request with the authentication token attached
    attachToken(request) {
        // determine token to attach
        let token = "";
        if(this.state.accessToken != null) {
            token = this.state.accessToken;
        } else if(this.state.refreshToken != null) {
            token = this.state.refreshToken;
        }
    
        // attach token by setting auth header in request
        if(token !== "") { 
            const headers = ("headers" in request) ? request.headers : {};
            headers["Authorization"] = `Bearer ${token}`;
            request.headers = headers;
        }

        return request;
    }
    
    
    /* CRUD operations */
    // query objects
    // type - type of object to query
    // params - query parameters to pass on query
    async query(type, params={}) {
        // check object type supported
        assert(this.supports(type));

        // build query url
        const queryParams = this.convertUrl(params);
        const queryUrl = `${this.objectUrl(type)}s${queryParams}`;
        // perform query request
        this.refresh();
        const response = await fetch(queryUrl, this.attachToken({}));
        await this.checkResponse(response);

        return await response.json();
    }

    // get object
    // type - type of object to get
    // id - id of the object to get
    async get(type, id) {
        // check object type supported
        assert(this.supports(type));

        const objUrl = `${this.objectUrl(type)}/${id}`;
    
        // perform get request
        this.refresh();
        const response = await fetch(objUrl, this.attachToken({
            method: "GET",
            mode: "cors",
            cache: "no-cache"
        }));
        await this.checkResponse(response);

        return await response.json();
    }

    // create  object
    // type - type of object to create
    // params - params to pass to create object
    // returns api response
    async post(type, params) {
        // check object type supported
        assert(this.supports(type));

        // perform create request 
        this.refresh();
        const response = await fetch(this.objectUrl(type), this.attachToken({
            method: "POST",
            mode: "cors",
            cache: "no-cache",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(params)
        }));
        await this.checkResponse(response);
        
        return await response.json();
    }
    
    // update object
    // type - type of object to update
    // id - id of the object to update
    // params - params to pass to update object
    // returns api response
    async update(type, id, params) {
        // check object type supported
        assert(this.supports(type));

        const objUrl = `${this.objectUrl(type)}/${id}`;

        // perform update request 
        this.refresh();
        const response = await fetch(objUrl, this.attachToken({
            method: "PATCH",
            mode: "cors",
            cache: "no-cache",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(params)
        }));
        await this.checkResponse(response);
        
        return await response.json();
    }

    // delete object
    // type - type of object to delete
    // id - id of the object to delete 
    // returns api response
    async delete(type, id) {
        // check object type supported
        assert(this.supports(type));

        // perform delete request
        const objUrl = `${this.objectUrl(type)}/${id}`;
        this.refresh();
        const response = await fetch(objUrl, this.attachToken({
            method: "DELETE",
            mode: "cors",
            cache: "no-cache"
        }));
        await this.checkResponse(response);
        
        return await response.json();
    }
}
